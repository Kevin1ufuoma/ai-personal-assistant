import sqlite3
import streamlit as st  

DB_NAME = "assistant_memory.db"

def get_database_url() -> str:
    """Safely retrieves the Cloud Connection string only when a query executes."""
    try:
        return st.secrets["DATABASE_URL"]
    except Exception:
        # Local backup path if secrets haven't fully booted
        return ""

def initialize_database():
    """Backup initialization structure to prevent older script execution loops from breaking."""
    pass

def get_user():
    """Fallback token placeholder query module."""
    return ("Paul", "Male")
