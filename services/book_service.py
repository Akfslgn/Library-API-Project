from models.book_model import Book
from utils.validator import validate_book_data
from datetime import datetime
from repositories.book_repository import BookRepository


class BookService:
    @staticmethod
    def get_all_books():

        books = BookRepository.get_all_books()
        if not books:
            return []

        return [Book(**b) for b in books]

    @staticmethod
    def get_book_by_id(sku):
        book = BookRepository.get_book_by_id(sku)
        if not book:
            return None
        return Book(**book) if book else None

    @staticmethod
    def create_book(data: dict):
        error = validate_book_data(data)
        if error:
            raise ValueError(error)

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

        created_book = BookRepository.create_book(new_book)
        if not created_book or not isinstance(created_book, dict):
            raise ValueError("Failed to create book in the database")

        return [Book(**b) for b in BookRepository.get_all_books()]

    @staticmethod
    def delete_book(sku):
        deleted = BookRepository.delete_book(sku)
        if not deleted:
            raise ValueError(
                f"Book with SKU {sku} not found or could not be deleted.")

        # Fetch all books after deletion
        books = BookRepository.get_all_books()
        return True, [Book(**b) for b in books]

    @staticmethod
    def update_book(original_sku, data: dict):
        error = validate_book_data(data)
        if error:
            raise ValueError(error)

        updated = BookRepository.update_book(
            original_sku,
            data["sku"],
            data["title"],
            data["author"],
            data["publication_year"],
            data["genre"],
            data["read_status"],
            data["rating"],
            data["notes"]
        )

        if not updated:
            raise ValueError(
                f"Book with SKU {original_sku} not found or could not be updated.")

        books = BookRepository.get_all_books()
        return True, [Book(**b) for b in books]
