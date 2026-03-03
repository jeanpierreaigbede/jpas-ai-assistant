# Assistant AI — Frontend

This is a minimal Next.js frontend for your Assistant AI backend. It provides:

- A home page with avatar, system name, description and a form to submit a PDF or a URL.
- A result page that fetches and displays an analysis summary and sources.

Setup

1. Copy environment variables into `.env.local` (or set in your environment):

```
NEXT_PUBLIC_API_BASE=http://localhost:8000
NEXT_PUBLIC_SYSTEM_NAME=Assistant AI
NEXT_PUBLIC_AVATAR_URL=/avatar-placeholder.png
NEXT_PUBLIC_SYSTEM_DESC=Upload a PDF or provide a URL to analyze it with the assistant.
```

2. Install and run:

```bash
cd web-app
npm install
npm run dev
```

API expectations

- POST `${NEXT_PUBLIC_API_BASE}/process` accepts multipart form with `file` or `url` and returns JSON `{ id: string }` (or an immediate result object).
- GET `${NEXT_PUBLIC_API_BASE}/result/:id` returns JSON containing `summary` and optional `sources`.

If your backend uses different endpoints, update `NEXT_PUBLIC_API_BASE` and adjust the client code in `components/UploadForm.tsx` and `pages/result/[id].tsx`.
