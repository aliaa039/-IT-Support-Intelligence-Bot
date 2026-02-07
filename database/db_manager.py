"""
Database operations: schema creation, connections, and query execution.
Uses only sqlite3 (no pandas) so database_setup works with minimal dependencies.
"""
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

try:
    from config import DATABASE_PATH
except ImportError:
    DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "support_tickets.db"


def _rows_to_dicts(cursor):
    """Convert cursor.fetchall() to list of dicts using column names."""
    cols = [d[0] for d in cursor.description] if cursor.description else []
    return [dict(zip(cols, row)) for row in cursor.fetchall()]


class DBManager:
    """Database operations and query execution for IT support tickets."""

    def __init__(self, db_path=None):
        self.db_path = db_path or DATABASE_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = None

    def connect(self):
        """Create database connection."""
        return sqlite3.connect(str(self.db_path))

    def create_tables(self):
        """Create the tickets table if it does not exist."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL,
                priority TEXT NOT NULL,
                category TEXT NOT NULL,
                assignee TEXT,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL,
                resolved_at TIMESTAMP,
                sla_deadline TIMESTAMP,
                customer_name TEXT,
                customer_email TEXT
            )
        """)
        conn.commit()
        conn.close()

    def execute_query(self, analysis, time_cutoff=None):
        """
        Execute a query based on analysis dict from query_processor.
        analysis: { type, status, priority, time_filter }
        """
        conn = self.connect()
        try:
            if analysis["type"] == "count":
                return self._count_query(conn, analysis, time_cutoff)
            if analysis["type"] == "trend":
                return self._trend_query(conn, analysis, time_cutoff)
            if analysis["type"] == "average":
                return self._average_query(conn, analysis, time_cutoff)
            if analysis["type"] == "sla":
                return self._sla_query(conn, analysis, time_cutoff)
            if analysis["type"] == "assignee":
                return self._assignee_query(conn, analysis, time_cutoff)
            if analysis["type"] == "performance":
                return self._performance_query(conn, analysis, time_cutoff)
            return self._general_query(conn, analysis, time_cutoff)
        finally:
            conn.close()

    def _time_filter_sql(self, time_filter, params, prefix="created_at"):
        if not time_filter or "days" not in time_filter:
            return "", params
        cutoff = datetime.now() - timedelta(days=time_filter["days"])
        return f" AND {prefix} >= ?", params + [cutoff]

    def _count_query(self, conn, analysis, time_cutoff=None):
        query = "SELECT status, priority, COUNT(*) as count FROM tickets WHERE 1=1"
        params = []
        if analysis.get("status"):
            query += " AND status = ?"
            params.append(analysis["status"])
        if analysis.get("priority"):
            query += " AND priority = ?"
            params.append(analysis["priority"])
        extra, params = self._time_filter_sql(analysis.get("time_filter"), params)
        query += extra + " GROUP BY status, priority"
        cur = conn.execute(query, params)
        rows = _rows_to_dicts(cur)
        total = sum(r["count"] for r in rows)
        return {
            "query_type": "count",
            "total": int(total),
            "breakdown": rows,
            "filters": analysis,
        }

    def _sla_query(self, conn, analysis, time_cutoff=None):
        query = """
            SELECT
                priority,
                COUNT(*) as total_tickets,
                SUM(CASE WHEN resolved_at IS NOT NULL AND resolved_at <= sla_deadline THEN 1 ELSE 0 END) as met_sla,
                SUM(CASE WHEN resolved_at IS NOT NULL AND resolved_at > sla_deadline THEN 1 ELSE 0 END) as missed_sla,
                SUM(CASE WHEN resolved_at IS NULL AND datetime('now') > sla_deadline THEN 1 ELSE 0 END) as overdue
            FROM tickets
            WHERE 1=1
        """
        params = []
        extra, params = self._time_filter_sql(analysis.get("time_filter"), params)
        query += extra + " GROUP BY priority"
        cur = conn.execute(query, params)
        return {"query_type": "sla", "sla_metrics": _rows_to_dicts(cur)}

    def _assignee_query(self, conn, analysis, time_cutoff=None):
        query = """
            SELECT
                assignee,
                COUNT(*) as total_tickets,
                SUM(CASE WHEN status = 'Open' THEN 1 ELSE 0 END) as open_tickets,
                SUM(CASE WHEN status = 'In Progress' THEN 1 ELSE 0 END) as in_progress,
                SUM(CASE WHEN status IN ('Resolved','Closed') THEN 1 ELSE 0 END) as resolved
            FROM tickets
            WHERE assignee IS NOT NULL
        """
        params = []
        extra, params = self._time_filter_sql(analysis.get("time_filter"), params)
        query += extra + " GROUP BY assignee ORDER BY total_tickets DESC"
        cur = conn.execute(query, params)
        return {"query_type": "assignee", "assignee_stats": _rows_to_dicts(cur)}

    def _performance_query(self, conn, analysis, time_cutoff=None):
        query = """
            SELECT
                priority,
                category,
                COUNT(*) as total_resolved,
                AVG((JULIANDAY(resolved_at) - JULIANDAY(created_at)) * 24) as avg_resolution_hours
            FROM tickets
            WHERE resolved_at IS NOT NULL
        """
        params = []
        extra, params = self._time_filter_sql(analysis.get("time_filter"), params)
        query += extra + " GROUP BY priority, category"
        cur = conn.execute(query, params)
        return {"query_type": "performance", "performance_metrics": _rows_to_dicts(cur)}

    def _trend_query(self, conn, analysis, time_cutoff=None):
        query = """
            SELECT
                DATE(created_at) as date,
                status,
                COUNT(*) as count
            FROM tickets
            WHERE 1=1
        """
        params = []
        extra, params = self._time_filter_sql(analysis.get("time_filter") or {"days": 30}, params)
        query += extra + " GROUP BY DATE(created_at), status ORDER BY date"
        cur = conn.execute(query, params)
        return {"query_type": "trend", "trend_data": _rows_to_dicts(cur)}

    def _average_query(self, conn, analysis, time_cutoff=None):
        query = """
            SELECT
                AVG((JULIANDAY(resolved_at) - JULIANDAY(created_at)) * 24) as avg_hours,
                COUNT(*) as total_resolved
            FROM tickets
            WHERE resolved_at IS NOT NULL
        """
        params = []
        extra, params = self._time_filter_sql(analysis.get("time_filter"), params)
        cur = conn.execute(query + extra, params)
        rows = _rows_to_dicts(cur)
        row = rows[0] if rows else {}
        return {
            "query_type": "average",
            "avg_resolution_hours": float(row.get("avg_hours", 0) or 0),
            "total_resolved": int(row.get("total_resolved", 0) or 0),
        }

    def _general_query(self, conn, analysis, time_cutoff=None):
        query = """
            SELECT status, priority, category, COUNT(*) as count
            FROM tickets
            WHERE 1=1
        """
        params = []
        extra, params = self._time_filter_sql(analysis.get("time_filter"), params)
        query += extra + " GROUP BY status, priority, category"
        cur = conn.execute(query, params)
        return {"query_type": "general", "summary": _rows_to_dicts(cur)}
