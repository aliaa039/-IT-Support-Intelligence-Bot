"""
NLP-style query processing: extract intent, status, priority, and time filters
from natural language questions. Used by the app to build analysis dict for DBManager.
"""
import re


def analyze_question(question: str) -> dict:
    """
    Analyze a natural language question and return:
    - type: count | trend | average | sla | assignee | performance | general
    - status: Open | In Progress | Resolved | Closed | Pending | None
    - priority: Low | Medium | High | Critical | None
    - time_filter: { days: int } | None
    """
    q = question.lower().strip()
    query_type = "general"
    if any(w in q for w in ["how many", "count", "number of"]):
        query_type = "count"
    elif any(w in q for w in ["trend", "over time"]):
        query_type = "trend"
    elif any(w in q for w in ["average", "mean", "resolution time"]):
        query_type = "average"
    elif any(w in q for w in ["sla", "deadline", "overdue", "compliance"]):
        query_type = "sla"
    elif any(w in q for w in ["who", "assignee", "workload", "team member"]):
        query_type = "assignee"
    elif any(w in q for w in ["performance", "resolve", "resolution", "slowest", "longest"]):
        query_type = "performance"

    status = None
    if "open" in q:
        status = "Open"
    elif "progress" in q or "in progress" in q:
        status = "In Progress"
    elif "resolved" in q:
        status = "Resolved"
    elif "closed" in q:
        status = "Closed"
    elif "pending" in q:
        status = "Pending"

    priority = None
    if "critical" in q:
        priority = "Critical"
    elif "high" in q:
        priority = "High"
    elif "medium" in q:
        priority = "Medium"
    elif "low" in q:
        priority = "Low"

    time_filter = _extract_time_filter(q)

    return {
        "type": query_type,
        "status": status,
        "priority": priority,
        "time_filter": time_filter,
    }


def _extract_time_filter(question: str) -> dict | None:
    """Extract time period from question (e.g. this week -> { days: 7 })."""
    if "today" in question:
        return {"days": 1}
    if "week" in question:
        return {"days": 7}
    if "month" in question:
        return {"days": 30}
    if "year" in question:
        return {"days": 365}
    m = re.search(r"(\d+)\s*(day|week|month)", question)
    if m:
        num = int(m.group(1))
        unit = m.group(2)
        mult = {"day": 1, "week": 7, "month": 30}
        return {"days": num * mult.get(unit, 1)}
    return None
