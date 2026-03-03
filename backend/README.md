# EIT Assistant

> **EIT** — Your personal AI assistant that reads and summarizes articles, so you don't have to.

EIT is an AI-powered article summarizer with a friendly personality. Paste a URL or upload a PDF, and EIT will give you a clean, insightful summary in seconds — powered by Claude (Anthropic).

---

## Features

- 🔗 **Summarize by URL** — Paste any article link and get an instant summary
- 📄 **Summarize PDF** — Upload a PDF document for extraction and summarization
- 🤖 **EIT Personality** — Consistent, warm, and insightful AI persona
- 🪵 **Structured Logging** — Full request/response logging for observability
- ⚠️ **Graceful Error Handling** — Clear, user-friendly error messages at every step
- 🚀 **Deployed on fly.io** — Always available, globally distributed

---

## Project Structure

```
eit-assistant/
├── backend/                  # FastAPI Python backend
│   ├── main.py               # Application entry point & all routes
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile            # Container definition
│   └── fly.toml              # fly.io deployment config
│
└── frontend/                 # Flutter frontend app
    └── ...
```

---

## Backend Setup (FastAPI)

### Prerequisites

- Python 3.12+
- An [Anthropic API key](https://console.anthropic.com/)

### Local Development

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/eit-assistant.git
cd eit-assistant/backend
```

**2. Create a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# or
.venv\Scripts\activate           # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set your API key**

```bash
export ANTHROPIC_API_KEY="sk-ant-..."   # macOS/Linux
# or
set ANTHROPIC_API_KEY=sk-ant-...        # Windows CMD
```

**5. Run the server**

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

Interactive API docs: `http://localhost:8000/docs`

---

## API Reference

### `GET /health`
Health check endpoint.

**Response:**
```json
{ "status": "ok", "version": "1.0.0" }
```

---

### `POST /summarize/url`
Summarize an article from a URL.

**Request body:**
```json
{ "url": "https://example.com/some-article" }
```

**Response:**
```json
{
  "summary": "EIT's summary here...",
  "source": "https://example.com/some-article",
  "char_count": 4821
}
```

---

### `POST /summarize/pdf`
Summarize an uploaded PDF file.

**Request:** `multipart/form-data` with a `file` field (PDF only, max 20MB)

**Response:**
```json
{
  "summary": "EIT's summary here...",
  "source": "my-document.pdf",
  "char_count": 12043
}
```

---

## Deployment on fly.io

### Prerequisites

- [flyctl installed](https://fly.io/docs/hands-on/install-flyctl/)
- A fly.io account

### Steps

**1. Authenticate**
```bash
fly auth login
```

**2. Set your Anthropic API key as a secret**
```bash
fly secrets set ANTHROPIC_API_KEY="sk-ant-..." --app eit-assistant-api
```

**3. Deploy**
```bash
cd backend
fly deploy
```

**4. Verify deployment**
```bash
fly status --app eit-assistant-api
curl https://eit-assistant-api.fly.dev/health
```

### First-time deployment (create the app)

If deploying for the first time:
```bash
fly launch --name eit-assistant-api --region iad --no-deploy
fly secrets set ANTHROPIC_API_KEY="sk-ant-..."
fly deploy
```

---

## Logging

All requests are logged with structured formatting:

```
2025-01-15 10:23:41 | INFO     | eit-assistant | POST /summarize/url | url=https://...
2025-01-15 10:23:41 | INFO     | eit-assistant | Fetching article from URL: https://...
2025-01-15 10:23:42 | INFO     | eit-assistant | Extracted 5243 characters from URL
2025-01-15 10:23:42 | INFO     | eit-assistant | Sending content to Claude for summarization | source=... | length=5243
2025-01-15 10:23:45 | INFO     | eit-assistant | Summary generated successfully | tokens_used=312
```

To view live logs on fly.io:
```bash
fly logs --app eit-assistant-api
```

---

## Error Handling

| Scenario | HTTP Status | Message |
|---|---|---|
| Invalid URL / unreachable page | 422 | "Could not fetch content from the provided URL" |
| Page requires login / no article content | 422 | "Could not extract readable article content" |
| Non-PDF file uploaded | 400 | "Only PDF files are accepted" |
| PDF too large (>20MB) | 413 | "PDF file is too large" |
| Scanned/image PDF | 422 | "No extractable text" |
| Anthropic API down | 503 | "AI service temporarily unavailable" |
| Rate limited | 429 | "Rate limit reached" |
| Unexpected error | 500 | "An unexpected error occurred" |

---

## About EIT

EIT is more than just a summarizer — it's an assistant with a personality. Sharp, concise, and always leaving you with something to think about.

---

*Built with ❤️ by EIT*
