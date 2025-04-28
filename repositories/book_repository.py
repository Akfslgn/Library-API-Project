from db import get_db
from psycopg2.extras import RealDictCursor


class BookRepository:
    @staticmethod
    def get_all_books():
        connection = get_db()
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT id, sku, title, author, publication_year, genre, read_status, rating, notes, created_at, uuid, updated_at FROM books")
            books = cursor.fetchall()
        return books

    @staticmethod
    def get_book_by_id(sku):
        connection = get_db()
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT id, sku, title, author, publication_year, genre, read_status, rating, notes, created_at, uuid, updated_at FROM books WHERE sku = %s", (sku,))
            book = cursor.fetchone()
        return book

    @staticmethod
    def get_book_by_title(title):
        connection = get_db()
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT id, sku, title, author, publication_year, genre, read_status, rating, notes, created_at, uuid, updated_at FROM books WHERE title = %s", (title,))
            book = cursor.fetchone()
        return book

    @staticmethod
    def create_book(book):
        connection = get_db()
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute(
                    """INSERT INTO books (sku, title, author, publication_year, genre, read_status, rating, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *""",
                    (book.sku, book.title, book.author, book.publication_year,
                     book.genre, book.read_status, book.rating, book.notes)
                )
                connection.commit()
                created_book = cursor.fetchone()
                if not created_book:
                    raise ValueError("Failed to create book in the database")
            except Exception as e:
                connection.rollback()
                raise ValueError(f"Database error: {str(e)}")
        return created_book

    @staticmethod
    def delete_book(sku):
        connection = get_db()
        with connection.cursor() as cursor:
            try:
                cursor.execute("DELETE FROM books WHERE sku = %s", (sku,))
                connection.commit()
                return cursor.rowcount > 0  # Return True if a row was deleted
            except Exception as e:
                connection.rollback()
                raise ValueError(f"Database error: {str(e)}")

    @staticmethod
    def update_book(original_sku, new_sku, title, author, publication_year, genre, read_status, rating, notes):
        connection = get_db()
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    UPDATE books
                    SET sku = %s, title = %s, author = %s, publication_year = %s,
                        genre = %s, read_status = %s, rating = %s, notes = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE sku = %s
                    """,
                    (new_sku, title, author, publication_year,
                     genre, read_status, rating, notes, original_sku)
                )
                connection.commit()
                return cursor.rowcount > 0  # Return True if a row was updated
            except Exception as e:
                connection.rollback()
                raise ValueError(f"Database error: {str(e)}")
