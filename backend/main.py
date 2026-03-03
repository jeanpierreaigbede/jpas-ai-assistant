"""
JPAS Assistant - Backend API
Author: JPAS
Description: FastAPI backend for JPAS Assistant - an AI-powered article summarizer
             supporting URL and PDF input with the JPAS personality.
             Powered by Google Gemini.
"""

import logging
import sys
import os
from contextlib import asynccontextmanager

import google.generativeai as genai
from dotenv import load_dotenv
import trafilatura
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import pymupdf  # PyMuPDF

load_dotenv()  # Loads GEMINI_API_KEY from .env file if present

# ─────────────────────────── Logging Setup ───────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("jpas-assistant")

# ─────────────────────────── Gemini Setup ────────────────────────────────────

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY is not set! Please set it in your .env file or environment.")

genai.configure(api_key=GEMINI_API_KEY)

# ─────────────────────────── JPAS Personality ─────────────────────────────────

JPAS_SYSTEM_PROMPT = """
You are JPAS — a sharp, friendly, and insightful AI assistant created by JPAS.
You have a passion for making complex information easy to understand.

Your personality:
- Warm but professional — you're knowledgeable without being condescending
- You speak clearly and confidently, getting straight to the point
- You occasionally show enthusiasm when content is particularly interesting
- You sign off summaries with a brief takeaway or reflection

When summarizing articles:
1. Start with a one-sentence summary of the main idea (do not use "TL;DR" or "TL;DR:" — just the sentence)
2. Cover the key points in clear, digestible language
3. Note any important context, caveats, or controversies
4. End with a brief personal takeaway from JPAS's perspective

Always identify yourself as JPAS if asked who you are.
"""

# ─────────────────────────── App Lifespan ────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 JPAS Assistant backend starting up...")
    yield
    logger.info("🛑 JPAS Assistant backend shutting down...")


# ─────────────────────────── FastAPI App ─────────────────────────────────────

app = FastAPI(
    title="JPAS Assistant API",
    description="AI-powered article summarizer with the JPAS personality",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────── Pydantic Models ─────────────────────────────────

class URLRequest(BaseModel):
    url: HttpUrl

class SummaryResponse(BaseModel):
    summary: str
    source: str
    char_count: int

class HealthResponse(BaseModel):
    status: str
    version: str

# ─────────────────────────── Helpers ─────────────────────────────────────────

def summarize_with_gemini(content: str, source_label: str) -> str:
    """Send content to Gemini 2.5 Flash with JPAS personality for summarization."""
    logger.info(f"Sending content to Gemini | source={source_label} | length={len(content)}")

    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=JPAS_SYSTEM_PROMPT,
        )
        response = model.generate_content(
            f"Please summarize the following article:\n\n{content[:12000]}"
        )
        summary = response.text
        logger.info(f"Summary generated successfully | chars={len(summary)}")
        return summary

    except Exception as e:
        logger.error(f"Gemini API error: {e}", exc_info=True)
        raise


def extract_article_from_url(url: str) -> str:
    """Fetch and extract clean article text from a URL using trafilatura."""
    logger.info(f"Fetching article from URL: {url}")

    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        logger.warning(f"trafilatura fetch failed for URL: {url}")
        raise HTTPException(
            status_code=422,
            detail="Could not fetch content from the provided URL. Please check the URL and try again.",
        )

    text = trafilatura.extract(downloaded)
    if not text or len(text.strip()) < 100:
        logger.warning(f"Insufficient content extracted from URL: {url}")
        raise HTTPException(
            status_code=422,
            detail="Could not extract readable article content from this URL. The page may require login or may not contain an article.",
        )

    logger.info(f"Extracted {len(text)} characters from URL")
    return text


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file using PyMuPDF."""
    logger.info(f"Extracting text from PDF | size={len(file_bytes)} bytes")

    try:
        doc = pymupdf.open(stream=file_bytes, filetype="pdf")
        text_parts = [page.get_text() for page in doc if page.get_text().strip()]
        doc.close()

        full_text = "\n\n".join(text_parts)

        if len(full_text.strip()) < 50:
            raise HTTPException(
                status_code=422,
                detail="The PDF appears to be empty or contains no extractable text (e.g. scanned image PDF).",
            )

        logger.info(f"Extracted {len(full_text)} characters from PDF ({len(text_parts)} pages with content)")
        return full_text

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PDF extraction failed: {e}", exc_info=True)
        raise HTTPException(status_code=422, detail=f"Failed to parse PDF: {str(e)}")


# ─────────────────────────── Routes ──────────────────────────────────────────

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint for fly.io and monitoring."""
    return HealthResponse(status="ok", version="1.0.0")


@app.post("/summarize/url", response_model=SummaryResponse, tags=["Summarize"])
async def summarize_url(request: URLRequest):
    """
    Summarize an article from a given URL.
    Fetches content via trafilatura, summarizes with Gemini 2.5 Flash + JPAS personality.
    """
    url_str = str(request.url)
    logger.info(f"POST /summarize/url | url={url_str}")

    try:
        article_text = extract_article_from_url(url_str)
        summary = summarize_with_gemini(article_text, source_label=url_str)
        return SummaryResponse(summary=summary, source=url_str, char_count=len(article_text))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in /summarize/url: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again.")


@app.post("/summarize/pdf", response_model=SummaryResponse, tags=["Summarize"])
async def summarize_pdf(file: UploadFile = File(...)):
    """
    Summarize an uploaded PDF file.
    Extracts text via PyMuPDF, summarizes with Gemini 2.5 Flash + JPAS personality.
    """
    logger.info(f"POST /summarize/pdf | filename={file.filename} | content_type={file.content_type}")

    if file.content_type not in ("application/pdf", "application/octet-stream"):
        logger.warning(f"Invalid file type uploaded: {file.content_type}")
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    try:
        file_bytes = await file.read()

        if len(file_bytes) > 20 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="PDF file is too large. Please upload a file under 20MB.")

        article_text = extract_text_from_pdf(file_bytes)
        summary = summarize_with_gemini(article_text, source_label=file.filename or "uploaded PDF")
        return SummaryResponse(summary=summary, source=file.filename or "uploaded PDF", char_count=len(article_text))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in /summarize/pdf: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again.")