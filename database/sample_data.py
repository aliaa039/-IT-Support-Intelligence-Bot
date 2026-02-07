"""Generate sample IT support tickets for demo/testing."""
import random
from datetime import datetime, timedelta
from pathlib import Path

try:
    from config import DATABASE_PATH
except ImportError:
    DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "support_tickets.db"

STATUSES = ["Open", "In Progress", "Resolved", "Closed", "Pending"]
PRIORITIES = ["Low", "Medium", "High", "Critical"]
CATEGORIES = [
    "Network Issue", "Hardware Problem", "Software Bug",
    "Access Request", "Email Issue", "Password Reset",
    "Printer Problem", "VPN Issue", "System Crash",
]
ASSIGNEES = [
    "Ahmed Hassan", "Sarah Ali", "Mohamed Khaled",
    "Fatima Ibrahim", "Omar Saeed", "Nour Mahmoud",
    None,
]
CUSTOMERS = [
    ("Ali Ahmed", "ali.ahmed@company.com"),
    ("Mona Salem", "mona.salem@company.com"),
    ("Khaled Nasser", "khaled.nasser@company.com"),
    ("Heba Fahmy", "heba.fahmy@company.com"),
    ("Youssef Magdy", "youssef.magdy@company.com"),
]
SLA_HOURS = {"Critical": 4, "High": 24, "Medium": 48, "Low": 72}


def generate_sample_tickets(db_path=None, num_tickets=200):
    """Insert sample tickets into the database. Creates table if needed."""
    import sqlite3
    db_path = db_path or DATABASE_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
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
    for i in range(num_tickets):
        days_ago = random.randint(0, 90)
        created_at = datetime.now() - timedelta(days=days_ago)
        status = random.choice(STATUSES)
        priority = random.choice(PRIORITIES)
        category = random.choice(CATEGORIES)
        assignee = random.choice(ASSIGNEES)
        customer = random.choice(CUSTOMERS)
        sla_deadline = created_at + timedelta(hours=SLA_HOURS[priority])
        updated_at = created_at + timedelta(hours=random.randint(1, 48))
        resolved_at = None
        if status in ("Resolved", "Closed"):
            resolved_at = updated_at + timedelta(hours=random.randint(1, 24))
        title = f"{category} - {customer[0]}"
        description = f"Customer reported: {category.lower()}. Priority: {priority}"
        cursor.execute("""
            INSERT INTO tickets (
                title, description, status, priority, category,
                assignee, created_at, updated_at, resolved_at,
                sla_deadline, customer_name, customer_email
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, description, status, priority, category,
              assignee, created_at, updated_at, resolved_at,
              sla_deadline, customer[0], customer[1]))
    conn.commit()
    conn.close()
    return num_tickets
