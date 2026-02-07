"""Unit tests for query processing and DB execution (no LLM)."""
import os
import sys
from pathlib import Path

# Run from project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.query_processor import analyze_question
from utils.analytics import format_db_results


def test_analyze_question_count_open():
    a = analyze_question("How many open tickets do we have?")
    assert a["type"] == "count"
    assert a["status"] == "Open"
    assert a["priority"] is None


def test_analyze_question_sla():
    a = analyze_question("What's the SLA compliance rate?")
    assert a["type"] == "sla"


def test_analyze_question_assignee():
    a = analyze_question("Who has the most open tickets?")
    assert a["type"] == "assignee"


def test_analyze_question_time_week():
    a = analyze_question("Tickets created this week")
    assert a["time_filter"] == {"days": 7}


def test_analyze_question_time_month():
    a = analyze_question("Critical tickets last month")
    assert a["priority"] == "Critical"
    assert a["time_filter"] == {"days": 30}


def test_format_db_results_count():
    r = {
        "query_type": "count",
        "total": 42,
        "breakdown": [{"status": "Open", "priority": "High", "count": 10}],
    }
    out = format_db_results(r)
    assert "42" in out
    assert "Open" in out
