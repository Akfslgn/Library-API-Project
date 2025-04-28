from app import create_app
from db import get_db, close_db


def create_tables():
    app = create_app()

    with app.app_context():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                sku VARCHAR(64) UNIQUE NOT NULL,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                publication_year INT NOT NULL,
                genre VARCHAR(100) NOT NULL,
                read_status VARCHAR(50) NOT NULL,
                rating FLOAT CHECK (rating >= 0 AND rating <= 5),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                uuid UUID DEFAULT gen_random_uuid() ,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cur.close()
        close_db()


if __name__ == "__main__":
    create_tables()
    print("✅ Table created successfully.")
