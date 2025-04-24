from db import book_data
from models.book_model import Book
from utils.validator import validate_book_data
from datetime import datetime


class BookService:
    @staticmethod
    def get_all_books():
        return book_data

    @staticmethod
    def get_book_by_id(sku: str):
        for book in book_data:
            if book.sku == sku:
                return book
        return None

    @staticmethod
    def create_book(data: dict):
        is_valid, error = validate_book_data(data)
        if not is_valid:
            raise ValueError(error)

        # Create a new book instance
        new_book = Book(
            sku=data.get("sku"),
            title=data.get("title"),
            author=data.get("author"),
            publication_year=data.get("publication_year"),
            genre=data.get("genre"),
            read_status=data.get("read_status"),
            rating=data.get("rating"),
            notes=data.get("notes"),
        )
        book_data.append(new_book)
        return new_book

    @staticmethod
    def delete_book(sku):
        for book in book_data:
            if book.sku == sku:
                book_data.remove(book)
                return True
        return False

    @staticmethod
    def update_book(sku, title, author, publication_year, genre, read_status, rating, notes):
        for book in book_data:
            if book.sku == sku:
                book.title = title
                book.author = author
                book.publication_year = publication_year
                book.genre = genre
                book.read_status = read_status
                book.rating = rating
                book.notes = notes
                book.updated_at = datetime.now()
                return True
        return False
