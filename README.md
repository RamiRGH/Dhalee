# Dhalee (ضليع) POC

A functional proof-of-concept for the Dhalee AI career transformation platform. Built for the **Agenticthon**.

**Bridging the Gap Between Potential and Professional Mastery.**

Upload your CV (PDF or DOCX), enter your desired role, and Dhalee's squad of 6 AI agents will autonomously audit your skills, scout the market, curate learning resources, and generate a personalized roadmap — culminating in a data-backed Readiness Report.

---

## What It Does

1. **Skill Auditor** — Deep semantic analysis of your CV to extract skills and identify exact gaps.
2. **Market Scout** — Real-time research of job market requirements aligned with your target role.
3. **Content Curator** — Mines the web for the best free learning resources per skill gap.
4. **Roadmap Architect** — Builds a structured, week-by-week learning journey.
5. **Performance Coach** — Reviews the roadmap for realism, prerequisites, and coverage.
6. **Talent Advocate** — Synthesizes everything into a Readiness Report for recruiters.

---

## Tech Stack

- **Backend**: FastAPI + LangGraph (multi-agent orchestration)
- **Frontend**: React + Vite + Tailwind CSS + react-i18next (EN / AR bilingual)
- **LLM**: OpenAI-compatible client (configurable via `.env`)
- **Search**: Tavily (swappable with Mock provider for offline testing)
- **Package Managers**: `uv` (Python), `npm` (Node)
- **State**: Fully stateless — no database, no auth

---

## Project Structure

```
dhalee-poc/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app + SSE streaming endpoint
│   │   ├── config.py            # Pydantic-settings from .env
│   │   ├── schemas.py           # DhaleeState TypedDict
│   │   ├── cv_parser/           # PDF/DOCX parsing + LLM ATS validation
│   │   ├── search/              # Swappable search providers (Tavily / Mock)
│   │   └── agents/              # 6 LangGraph agent nodes + graph wiring
│   ├── pyproject.toml
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   ├── InputSection.tsx
│   │   │   ├── ProgressTracker.tsx
│   │   │   ├── RoadmapView.tsx
│   │   │   └── ReadinessReport.tsx
│   │   └── i18n.ts
│   └── public/locales/          # EN + AR translations
├── .gitignore
└── README.md
```

---

## Setup

### Prerequisites

- Python 3.10+ with [uv](https://docs.astral.sh/uv/)
- Node.js 18+ with npm

### 1. Backend

```bash
cd backend
cp .env.example .env
# Edit .env and add your API keys
uv sync
```

**Required `.env` values:**

```bash
OPENAI_API_KEY=your-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o

# Optional: for real web search
TAVILY_API_KEY=your-key-here
SEARCH_PROVIDER=mock
```

**Run backend:**

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend dev server proxies `/api` requests to `http://localhost:8000` automatically.

### 3. Use It

Open `http://localhost:5173`, upload a CV, enter a desired role, and watch the agent squad work in real time.

---

## How to Switch LLM Provider

Because the backend uses the official `openai` client, you can drop in any OpenAI-compatible endpoint. Just update `backend/.env` and restart.

Examples:
- **OpenAI**: `OPENAI_BASE_URL=https://api.openai.com/v1`
- **Groq**: `OPENAI_BASE_URL=https://api.groq.com/openai/v1`
- **Together AI**: `OPENAI_BASE_URL=https://api.together.xyz/v1`
- **Local (vLLM / Ollama)**: `OPENAI_BASE_URL=http://localhost:11434/v1`

> **Note**: Dhalee sends long prompts and expects large structured JSON outputs. Small models may hit their output token limit. If you see `finish_reason=length` errors, switch to a model with a larger output window.

---

## How to Switch Search Provider

The search module is a black box. Two providers are included:

- `tavily` — Real web search (requires `TAVILY_API_KEY`)
- `mock` — Returns placeholder results (works offline)

Change `SEARCH_PROVIDER` in `.env` to swap. To add a new provider:

1. Create `app/search/my_provider.py` implementing the `SearchProvider` interface.
2. Register it in `app/search/__init__.py`.

---

## Bilingual Support

The frontend supports **English** and **Arabic** with a language switcher in the header. It dynamically switches text direction (`ltr` / `rtl`) and loads translations from `public/locales/`.

---

## Notes

- **No database** — completely stateless. One request = one full agent pipeline.
- **No auth** — open access, designed for demo/POC use.
- **CV validation** — parsed text is checked by an LLM to ensure it looks like a real CV. If not, the user gets a clear error about ATS compatibility.
