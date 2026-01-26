# 🤖 IT Support Intelligence Bot

AI-powered system for analyzing IT support tickets using natural language queries.

---

## 📌 Overview

**IT Support Intelligence Bot** is a smart conversational system that helps teams analyze IT support tickets without writing manual queries or navigating complex dashboards.

Users can ask questions in plain English and get clear insights about ticket status, performance, SLA compliance, and team workload.

---

## ✨ Key Features

* **Natural Language Queries**
  Ask questions like:

  * *How many open tickets do we have?*
  * *Which category takes the longest to resolve?*

* **Multi-Agent Architecture**

  * Query understanding
  * Role-based customization
  * Data retrieval
  * Analytics & insights generation

* **Role Awareness**

  * **Support Agent** → operational answers
  * **Team Lead** → performance & workload
  * **Manager** → high-level insights

* **Analytics**

  * Ticket status & priority distribution
  * SLA compliance
  * Resolution time analysis
  * Bottleneck detection

* **Interactive UI**

  * Built with **Streamlit**
  * Conversation history
  * Example questions

---

## 🏗️ Architecture

```
Streamlit UI
     │
Query Executor
     │
SQLite Database
     │
Multi-Agent System (CrewAI + LLaMA)
```

---

## ⚙️ Tech Stack

* Python 3.8+
* Streamlit
* SQLite
* CrewAI (Multi-Agent system)
* LLaMA models via Groq API

---

## 🚀 Installation & Run

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup database
python database_setup.py

# Run app
streamlit run app.py
```

Create a `.env` file and add:

```env
GROQ_API_KEY=your_api_key_here
```

---

## 💬 Example Questions

* “How many open tickets do we have?”
* “What’s the SLA compliance rate?”
* “Who has the highest workload?”
* “Which category has the slowest resolution time?”

---

## 📁 Project Structure

```
it-support-bot/
│
├── app.py
├── agents.py
├── query_executor.py
├── database_setup.py
├── requirements.txt
├── it_support.db
└── README.md
```

---

## 🔮 Future Improvements

* Integration with Jira / ServiceNow
* Export reports (PDF, Excel)
* Charts and dashboards
* Alerting system
* Arabic language support





