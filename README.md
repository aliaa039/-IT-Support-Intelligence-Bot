# 🤖 IT Support Intelligence Bot

A multi-agent AI system for analyzing IT support tickets using natural language.

---

## 📋 Overview

IT Support Intelligence Bot is an AI-powered system that converts IT support ticket data into clear insights through a conversational interface.

Instead of dashboards and manual queries, users can ask questions in natural language and receive actionable answers.

---

## 🎯 Problem

Traditional IT support systems:

* Depend on complex dashboards
* Require manual queries
* Provide raw data with little insight

This results in slower decisions and inefficient operations.

---

## 💡 Solution

A conversational AI bot that:

* Understands natural language questions
* Identifies user role
* Retrieves and analyzes ticket data
* Returns meaningful insights, not just numbers

---

## 🌟 Features

### • Natural Language Queries

Ask questions like:

* “How many open tickets do we have?”
* “Which category takes the longest to resolve?”

### • Multi-Agent System

* Query understanding
* Role awareness
* Data retrieval
* Analytics
* Response generation

### • Role Awareness

* **Support Agent**: operational answers
* **Team Lead**: team performance
* **Manager**: high-level insights

### • Analytics

* Ticket status & priority
* SLA compliance
* Resolution time
* Workload distribution

### • Streamlit Interface

* Interactive UI
* Example questions
* Conversation history

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

## 💻 Installation

```bash
python -m venv venv
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python database_setup.py
streamlit run app.py
```

Create a `.env` file:

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
├── app.py
├── agents.py
├── query_executor.py
├── database_setup.py
├── requirements.txt
├── it_support.db
└── README.md
```


