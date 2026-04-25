# Dhalee (ضليع) 🚀
**Bridging the Gap Between Potential and Professional Mastery.**

Dhalee AI is an advanced **Multi-Agent System (MAS)** built for the **Agenticthon**. It empowers the Saudi workforce by autonomously identifying skill gaps, generating personalized learning roadmaps from open-source content, and verifying professional readiness for the local job market.

---

## 🛠 Tech Stack
- **AI Orchestration:** [CrewAI](https://www.crewai.com/), [LangChain](https://www.langchain.com/)
- **LLMs:** OpenAI (GPT-4o), Groq (Llama-3 for fast inference)
- **Backend:** Python, FastAPI
- **Frontend:** React, Tailwind CSS
- **Vector Database:** ChromaDB (RAG implementation)
- **Search:** Tavily Search API (Agent-optimized search)

---

## 🤖 The Agentic Squad (Dhalee Crew)
Dhalee operates through a coordinated squad of **six autonomous agents**, each with a specific role in the user's career transformation:

1.  **The Skill Auditor:** Performs deep semantic analysis of CVs to detect latent expertise and exact skill deltas.
2.  **The Market Scout:** Real-time scouting of the Saudi job market and Vision 2030 hiring trends.
3.  **The Content Curator:** Mines and filters the best free educational resources (YouTube, Coursera, MOOCs).
4.  **The Roadmap Architect:** Constructs structured, pedagogical, week-by-week learning journeys.
5.  **The Performance Coach:** Manages the **Feedback Loop**, validates progress via micro-assessments, and refines the roadmap.
6.  **The Talent Advocate:** Synthesizes progress into a **Readiness Report** for recruiters.

---

## 🏗 System Architecture (Agentic Workflow)
```mermaid
graph TD
    A[User CV & Target Job] --> B(Dhalee Auditor)
    B --> C{Skill Gap Identified?}
    C -->|Yes| D(Dhalee Scout & Curator)
    D --> E(Dhalee Architect)
    E --> F(Dhalee Coach)
    F --> G(Continuous Feedback Loop)
    G --> H(Dhalee Advocate)
    H --> I[Verified Readiness Report]
'''
