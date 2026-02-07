"""
Standalone script to create the database and populate sample tickets.
Run once: python database_setup.py
Or the app will auto-create on first run.
"""
from config import DATABASE_PATH
from database.db_manager import DBManager
from database.sample_data import generate_sample_tickets

def main():
    print("🚀 IT Support Bot - Database setup\n")
    DBManager().create_tables()
    n = generate_sample_tickets(num_tickets=200)
    print(f"✅ Created {DATABASE_PATH}")
    print(f"✅ Inserted {n} sample tickets.")
    print("\n✨ Done. To run the app: pip install -r requirements.txt then python -m streamlit run app.py")

if __name__ == "__main__":
    main()
