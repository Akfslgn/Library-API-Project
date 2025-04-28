import psycopg2
from flask import g, current_app


def get_db():
    """Get a database connection."""
    if 'db' not in g:
        g.db = psycopg2.connect(
            port="5432",
            host="localhost",
            dbname="flask_postgres_db",
            user="postgres",
            password="postgres",
        )
    return g.db


def close_db(e=None):
    """Close the database connection."""
    db = g.pop('db', None)
    if db is not None:
        db.close()
