# Assistant AI

> Application d'assistance IA pour résumer des articles à partir d'une URL ou d'un fichier PDF.

Assistant AI (JPAS Assistant) est une application full-stack qui permet de soumettre une URL ou un PDF et d'obtenir un résumé structuré via Google Gemini.

---

## Structure du projet

```
assistant_ai/
├── backend/           # API FastAPI (Python)
│   ├── main.py        # Point d'entrée et routes
│   ├── requirements.txt
│   ├── Dockerfile
│   └── fly.toml       # Déploiement fly.io
│
├── web-app/           # Interface Next.js (React)
│   ├── pages/         # Pages et composants
│   ├── components/
│   └── package.json
│
├── vercel.json        # Déploiement Vercel (web-app)
└── README.md
```

---

## Prérequis

- **Backend :** Python 3.12+, clé API [Google Gemini](https://makersuite.google.com/app/apikey)
- **Web-app :** Node.js 18+

---

## Installation et exécution

### 1. Backend (API)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
# ou  .venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

Créer un fichier `.env` à la racine de `backend/` avec :

```
GEMINI_API_KEY=votre_cle_api
```

Lancer le serveur :

```bash
uvicorn main:app --reload --port 8000
```

L'API est disponible sur `http://localhost:8000` — documentation interactive : `http://localhost:8000/docs`

---

### 2. Web-app (interface)

```bash
cd web-app
npm install
```

Créer un fichier `.env.local` avec :

```
NEXT_PUBLIC_API_BASE=http://localhost:8000
NEXT_PUBLIC_SYSTEM_NAME=JPAS Assistant
NEXT_PUBLIC_AVATAR_URL=/avatar-placeholder.png
NEXT_PUBLIC_SYSTEM_DESC=Uploadez un PDF ou collez une URL pour obtenir un résumé.
```

Lancer l'application :

```bash
npm run dev
```

L'interface est disponible sur `http://localhost:3000`

---

## Déploiement

- **Backend :** fly.io — voir `backend/README.md` et `fly.toml`
- **Web-app :** Vercel — configuré via `vercel.json` (root: `web-app`)

---

## Documentation détaillée

- [Backend — API, logs, gestion d'erreurs](backend/README.md)
- [Web-app — configuration frontend](web-app/README.md)
