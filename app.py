"""
Main Streamlit app for IT Support Intelligence Bot.
Uses config, database, utils, and agents packages.
"""
import os
import json
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Project imports
from config import LLM_PROVIDER, GROQ_API_KEY, DATABASE_PATH, SUPPORT_ROLES
from database.db_manager import DBManager
from database.sample_data import generate_sample_tickets
from utils.query_processor import analyze_question
from utils.analytics import format_db_results, results_to_json_string

try:
    from agents.crew_setup import ITSupportCrew
    AGENTS_AVAILABLE = True
except Exception as e:
    AGENTS_AVAILABLE = False
    _agents_error = str(e)

st.set_page_config(
    page_title="IT Support Intelligence Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_role" not in st.session_state:
    st.session_state.user_role = "Support Agent"


def ensure_database():
    """Create DB and sample data if missing (first run)."""
    if not DATABASE_PATH.exists():
        from database.db_manager import DBManager
        db = DBManager()
        db.create_tables()
        generate_sample_tickets(num_tickets=200)
        st.sidebar.success("✅ Sample database created with 200 tickets.")


def check_llm_setup():
    """Check if LLM is configured (Groq or Ollama)."""
    if LLM_PROVIDER == "ollama":
        return True, "ollama"
    if GROQ_API_KEY:
        return True, "groq"
    return False, None


def render_sidebar():
    st.sidebar.title("⚙️ Settings")
    st.sidebar.subheader("👤 Your Role")
    role = st.sidebar.selectbox(
        "Select your role:",
        SUPPORT_ROLES,
        index=SUPPORT_ROLES.index(st.session_state.user_role),
    )
    st.session_state.user_role = role
    with st.sidebar.expander("ℹ️ Role Information"):
        st.write("""
        **Support Agent**: Quick, actionable answers  
        **Team Lead**: Team performance insights  
        **Manager**: Strategic overview
        """)
    st.sidebar.divider()
    st.sidebar.subheader("💡 Example Questions")
    examples = {
        "📊 General": [
            "How many tickets are currently open?",
            "What's the total number of tickets?",
            "Show me ticket breakdown by status",
        ],
        "⚡ Priority": [
            "How many critical tickets do we have?",
            "Show me high priority tickets",
            "What's the distribution by priority?",
        ],
        "⏱️ Performance": [
            "What's the average resolution time?",
            "Show me performance metrics",
            "Which category takes longest to resolve?",
        ],
        "📅 SLA": [
            "What's our SLA compliance rate?",
            "How many tickets are overdue?",
            "Show me SLA violations this week",
        ],
        "👥 Assignees": [
            "Who has the most open tickets?",
            "Show me assignee workload",
            "Which team member resolved most tickets?",
        ],
    }
    for cat, questions in examples.items():
        with st.sidebar.expander(cat):
            for q in questions:
                if st.button(q, key=f"ex_{hash(q)}", use_container_width=True):
                    st.session_state.selected_question = q
    st.sidebar.divider()
    if st.sidebar.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    with st.sidebar.expander("ℹ️ System Information"):
        has_llm, provider = check_llm_setup()
        st.write(f"""
        **LLM**: {provider or "Not set"}  
        **Database**: {DATABASE_PATH.name}  
        **Role**: {st.session_state.user_role}  
        **Conversations**: {len(st.session_state.chat_history)}
        """)


def process_question(question: str, role: str):
    """Run query pipeline: analyze -> DB -> agents (or fallback)."""
    with st.spinner("🤔 Thinking..."):
        analysis = analyze_question(question)
        db = DBManager()
        db_results = db.execute_query(analysis)
        formatted = results_to_json_string(db_results)
        if AGENTS_AVAILABLE:
            try:
                crew = ITSupportCrew()
                response = crew.process_question(
                    question=question,
                    role=role,
                    db_results=formatted,
                )
                return response, db_results
            except Exception as e:
                response = (
                    f"📊 **Results:**\n\n{format_db_results(db_results)}\n\n"
                    f"⚠️ AI unavailable: {e}"
                )
                return response, db_results
        response = (
            f"📊 **Results:**\n\n{format_db_results(db_results)}\n\n"
            "💡 Add GROQ_API_KEY to .env or set LLM_PROVIDER=ollama for AI responses."
        )
        return response, db_results


def main():
    ensure_database()
    st.title("🤖 IT Support Intelligence Bot")
    st.markdown("**Multi-Agent AI for IT Support Ticket Analysis**")
    render_sidebar()

    has_llm, provider = check_llm_setup()
    if not has_llm:
        st.warning(
            "⚠️ Running in basic mode. Set GROQ_API_KEY in .env or use LLM_PROVIDER=ollama for AI."
        )

    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat["question"])
        with st.chat_message("assistant"):
            st.write(chat["response"])
            if chat.get("data"):
                with st.expander("📊 View Detailed Data"):
                    st.json(chat["data"])

    default_q = ""
    if "selected_question" in st.session_state:
        default_q = st.session_state.selected_question
        del st.session_state.selected_question

    question = st.chat_input("Ask about IT support tickets...", key="q_input")
    if default_q:
        question = question or default_q

    if question:
        with st.chat_message("user"):
            st.write(question)
        response, data = process_question(question, st.session_state.user_role)
        with st.chat_message("assistant"):
            st.write(response)
            with st.expander("📊 View Detailed Data"):
                st.json(data)
        st.session_state.chat_history.append({
            "question": question,
            "response": response,
            "data": data,
            "role": st.session_state.user_role,
            "timestamp": datetime.now().isoformat(),
        })

    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Current Role", st.session_state.user_role)
    with c2:
        st.metric("Conversations", len(st.session_state.chat_history))
    with c3:
        st.metric("System", "🟢 Active" if has_llm else "🟡 Basic Mode")


if __name__ == "__main__":
    main()
