"""Analytics helpers: format DB results for display and compute derived metrics."""
import json
from datetime import datetime


def format_db_results(results: dict) -> str:
    """Format database result dict into human-readable text (e.g. for fallback when no LLM)."""
    if results.get("query_type") == "count":
        out = f"**Total Tickets**: {results.get('total', 0)}\n\n"
        if results.get("breakdown"):
            out += "**Breakdown**:\n"
            for item in results["breakdown"]:
                out += f"- {item.get('status', '')} ({item.get('priority', '')}): {item.get('count', 0)}\n"
        return out
    if results.get("query_type") == "sla" and results.get("sla_metrics"):
        out = "**SLA Metrics**:\n"
        for row in results["sla_metrics"]:
            met = row.get("met_sla", 0) or 0
            total = row.get("total_tickets", 0) or 0
            rate = (met / total * 100) if total else 0
            out += f"- {row.get('priority', '')}: {rate:.1f}% met SLA ({met}/{total})\n"
        return out
    if results.get("query_type") == "assignee" and results.get("assignee_stats"):
        out = "**Assignee Workload**:\n"
        for row in results["assignee_stats"]:
            out += f"- {row.get('assignee', '')}: {row.get('total_tickets', 0)} total, {row.get('open_tickets', 0)} open\n"
        return out
    if results.get("query_type") == "performance" and results.get("performance_metrics"):
        out = "**Performance (avg resolution hours)**:\n"
        for row in results["performance_metrics"]:
            avg = row.get("avg_resolution_hours") or 0
            out += f"- {row.get('category', '')} ({row.get('priority', '')}): {avg:.1f}h\n"
        return out
    return json.dumps(results, indent=2, default=str)


def results_to_json_string(results: dict) -> str:
    """Convert results to JSON string for agent context."""
    return json.dumps(results, indent=2, default=str)
