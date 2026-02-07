"""
CrewAI crew setup: build LLM (Groq or Ollama), create crew, and process questions.
100% free: use Groq (free tier) or Ollama (local, no API key).
"""
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from crewai import Task, Crew, Process

from agents.agents_config import (
    create_query_agent,
    create_role_agent,
    create_analytics_agent,
    create_response_agent,
)

# Config
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower().strip()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


def _get_llm():
    """Return CrewAI-compatible LLM: Groq (free cloud) or Ollama (free local)."""
    if LLM_PROVIDER == "ollama":
        try:
            try:
                from langchain_community.chat_models import ChatOllama
            except ImportError:
                from langchain_community.chat_models.ollama import ChatOllama
            llm = ChatOllama(
                base_url=OLLAMA_BASE_URL,
                model=OLLAMA_MODEL,
                temperature=0.3,
            )
            return llm
        except Exception as e:
            raise RuntimeError(
                f"Ollama not available. Install Ollama from https://ollama.ai and run 'ollama pull {OLLAMA_MODEL}'. Error: {e}"
            )
    # Default: Groq (free tier)
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not set. Add it to .env or use LLM_PROVIDER=ollama for 100% local."
        )
    from langchain_groq import ChatGroq
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model_name=GROQ_MODEL,
        temperature=0.3,
    )


class ITSupportCrew:
    """Multi-agent crew for IT support ticket analysis."""

    def __init__(self, llm=None):
        self.llm = llm or _get_llm()

    def process_question(self, question: str, role: str = "Support Agent", db_results: str = None) -> str:
        """Run the crew and return the final response."""
        query_agent = create_query_agent(self.llm)
        role_agent = create_role_agent(self.llm)
        analytics_agent = create_analytics_agent(self.llm)
        response_agent = create_response_agent(self.llm)

        task1 = Task(
            description=f'''Analyze this question: "{question}"
            Extract: 1) What is the user asking for? 2) What filters are mentioned? 3) What analysis is needed?
            Provide a structured understanding.''',
            agent=query_agent,
            expected_output="Structured analysis of the question intent and filters",
        )
        task2 = Task(
            description=f'''User role: {role}. Based on the query understanding, determine:
            1) How detailed should the response be? 2) What recommendations? 3) Technical detail level?''',
            agent=role_agent,
            expected_output="Guidelines for response depth and format based on role",
        )
        task3 = Task(
            description=f'''Analyze this data and compute relevant metrics, insights, and concerns:\n{db_results or "No data"}''',
            agent=analytics_agent,
            expected_output="Data analysis with insights and metrics",
        )
        task4 = Task(
            description=f'''Create a final response for: "{question}"
            Use: query understanding, role guidelines, and analytics. Be clear, conversational, and actionable.''',
            agent=response_agent,
            expected_output="Final conversational response for the user",
        )

        crew = Crew(
            agents=[query_agent, role_agent, analytics_agent, response_agent],
            tasks=[task1, task2, task3, task4],
            process=Process.sequential,
            verbose=True,
        )
        result = crew.kickoff()
        return str(result)
