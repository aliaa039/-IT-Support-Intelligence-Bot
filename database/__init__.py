"""Database package: schema, operations, and sample data."""
from database.db_manager import DBManager
from database.sample_data import generate_sample_tickets

__all__ = ["DBManager", "generate_sample_tickets"]
