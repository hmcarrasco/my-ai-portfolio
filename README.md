# My AI Portfolio

A personal portfolio built to learn React while showcasing AI engineering skills. Rather than a traditional static portfolio, I wanted something that reflects what an AI engineer actually does — so the core features are a very simple **RAG-powered chatbot** that answers questions about my background and experience, and an **automated documentation generator** that pulls source code from GitHub repos and uses LLMs to produce technical docs.

## Tech Stack

- **Frontend:** React 19, TypeScript, Vite, Tailwind CSS 4
- **Backend:** FastAPI, Python 3.12, OpenAI (gpt-4o-mini), ChromaDB
- **CI:** GitHub Actions (lint, test, frontend-lint, frontend-test)
- **Hosting:** Render (Web Service + Static Site)

## Project Structure

```
├── ai/                  # Backend (FastAPI)
│   ├── api/             # Routes, schemas, middleware
│   ├── clients/         # OpenAI, GitHub, RAG, doc generator
│   ├── config/          # Settings, projects.yaml
│   ├── core/            # Chat service, RAG manager
│   ├── data/            # Personal data, docs cache
│   ├── prompts/         # System prompts (YAML)
│   ├── tests/           # Pytest test suite
│   └── utils/           # Logger, loaders
├── frontend/            # Frontend (React + Vite)
│   ├── src/
│   │   ├── components/  # Header, Footer
│   │   ├── contexts/    # Theme, Chat, Docs
│   │   ├── pages/       # Home, Chat, Docs, NotFound
│   │   ├── services/    # API clients
│   │   └── tests/       # Vitest test suite
│   └── public/
└── render.yaml          # Render deployment blueprint
```

## Local Development

### Prerequisites

- Python 3.12+
- Node.js 20+
- OpenAI API key

### Setup

```bash
# Clone
git clone https://github.com/hmcarrasco/my-ai-portfolio.git
cd my-ai-portfolio

# Backend
python -m venv venv && source venv/bin/activate
pip install -r ai/requirements.txt
cp ai/config/.env.template ai/config/.env
# Edit ai/config/.env with your OPENAI_API_KEY and GITHUB_OWNER

# Frontend
cd frontend && npm install
# Edit frontend/.env → VITE_API_URL=http://localhost:8000
```

### Run

```bash
# Backend (from project root)
uvicorn ai.api.main:app --reload

# Frontend (from frontend/)
npm run dev
```

### Test & Lint

```bash
make test          # Backend tests
make ruff          # Backend lint + format
make fe-test       # Frontend tests
make fe-lint       # Frontend lint
```

## Deploy to Render

This repo includes a [render.yaml](render.yaml) for one-click deployment.

### Steps

1. Push this repo to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com) → **New** → **Blueprint**
3. Connect your GitHub repo and select the `render.yaml`
4. Set the required environment variables:

| Service  | Variable          | Value                                                               |
| -------- | ----------------- | ------------------------------------------------------------------- |
| Backend  | `OPENAI_API_KEY`  | Your OpenAI key                                                     |
| Backend  | `ALLOWED_ORIGINS` | Your frontend URL (e.g., `https://my-ai-portfolio.onrender.com`)    |
| Frontend | `VITE_API_URL`    | Your backend URL (e.g., `https://my-ai-portfolio-api.onrender.com`) |

5. In the backend service, go to **Environment** → **Secret Files** → add a file at path `/etc/secrets/my-data.txt` with your personal info for the chatbot
6. Deploy!
