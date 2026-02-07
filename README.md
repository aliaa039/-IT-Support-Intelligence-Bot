# 🤖 IT Support Intelligence Bot

A multi-agent AI system for analyzing IT support tickets using **natural language**. Ask questions in plain English and get actionable answers—no SQL or dashboards required. Fully free: use **Groq** (free cloud) or **Ollama** (100% local).

---

## Overview

| | |
|---|---|
| **Problem** | Traditional IT support tools rely on dashboards and manual queries, slowing decisions. |
| **Solution** | A conversational bot that understands questions, pulls ticket data, and returns clear insights. |
| **Tech** | Streamlit, CrewAI, LangChain, SQLite. Optional: Groq or Ollama for AI responses. |

---

## Features

- **Natural language queries** — e.g. *"How many open tickets?"*, *"Who has the highest workload?"*
- **Role-aware answers** — Support Agent (actionable), Team Lead (team performance), Manager (strategic)
- **Multi-agent pipeline** — Query understanding → Role awareness → Analytics → Response generation
- **Streamlit UI** — Chat, example questions, conversation history, expandable data
- **Runs without AI** — Basic mode returns DB results only if no API key or Ollama

---

## Project Structure

```
it_support_bot/
├── .env.example          # Copy to .env and add API key or set Ollama
├── .gitignore
├── README.md
├── config.py             # DB path, LLM provider (groq/ollama), roles
├── app.py                # Main Streamlit app
├── database_setup.py     # Create DB + 200 sample tickets
├── requirements.txt      # Full stack (Streamlit, CrewAI, LangChain, etc.)
├── requirements-minimal.txt   # DB setup only (e.g. Python 3.14)
├── run.bat               # Windows: run Streamlit with venv
├── check_setup.py         # Check Python version and next steps
│
├── agents/
│   ├── __init__.py
│   ├── crew_setup.py     # CrewAI crew + Groq/Ollama LLM
│   └── agents_config.py  # Agent roles and backstories
│
├── database/
│   ├── __init__.py
│   ├── db_manager.py     # Schema + query execution (sqlite3 only)
│   └── sample_data.py     # Sample ticket generator
│
├── utils/
│   ├── __init__.py
│   ├── query_processor.py # NLP: intent, status, priority, time filters
│   └── analytics.py       # Format results for display
│
├── data/
│   └── support_tickets.db # SQLite DB (created by database_setup or app)
│
└── tests/
    ├── __init__.py
    └── test_queries.py    # Unit tests for query_processor & analytics
```

---

## Quick Start

**Recommended: Python 3.11 or 3.12.** (Python 3.14 can run DB setup only; see [Minimal install](#minimal-install-python-314).)

```bash
# Clone and enter project
cd IT_Support_Bot

# Create and activate venv (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create DB and 200 sample tickets (or skip; app creates on first run)
python database_setup.py

# Run the app
python -m streamlit run app.py
```

Then open the URL shown in the terminal (e.g. `http://localhost:8501`).

---

## Configuration

Copy `.env.example` to `.env` and choose one:

**Option A — Groq (free cloud)**  
Get a key at [console.groq.com](https://console.groq.com).

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_key_here
```

**Option B — Ollama (100% local, no key)**  
Install [Ollama](https://ollama.ai), then run `ollama pull llama3.2`.

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
```

**No .env / no key** — App runs in **basic mode**: DB answers only, no AI.

---

## Example Questions

- How many open tickets do we have?
- What’s the SLA compliance rate?
- Who has the most open tickets?
- Which category takes the longest to resolve?
- How many critical tickets were created this week?

---

## Minimal install (Python 3.14)

If you’re on Python 3.14, the full stack may fail (numpy/LangChain). You can still create the database:

```bash
pip install -r requirements-minimal.txt
python database_setup.py
```

For the full app (Streamlit + AI), use a venv with Python 3.11 or 3.12:

```bash
py -3.12 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py
```

---

## Tests

```bash
pip install -r requirements.txt   # or at least pytest
python -m pytest tests/ -v
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `streamlit` not recognized | Run `python -m streamlit run app.py` (or use `run.bat` on Windows). |
| `ModuleNotFoundError: pandas` / numpy build fails | Use Python 3.11 or 3.12, or run only `requirements-minimal.txt` + `database_setup.py`. |
| No AI responses | Set `GROQ_API_KEY` in `.env` or use `LLM_PROVIDER=ollama` with Ollama running. |
| DB not found | Run `python database_setup.py` or start the app once (it creates the DB automatically). |

---

## License

Use and modify freely. No warranty.
