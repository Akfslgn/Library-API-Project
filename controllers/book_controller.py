from flask import Blueprint, jsonify, request
from services.book_service import BookService

book_bp = Blueprint("book", __name__, url_prefix="/api/v1")


@book_bp.route("/books", methods=["GET"])
def get_all_books():
    """
    Get all books.
    """
    books = BookService.get_all_books()
    return jsonify([book.to_dict() for book in books]), 200


@book_bp.route("/books/<string:sku>", methods=["GET"])
def get_book(sku):
    """
    Get a book by sku.
    """
    book = BookService.get_book_by_id(sku)
    if book:
        return jsonify(book.to_dict()), 200
    return jsonify({"error": "Book not found"}), 404


@book_bp.route("/books", methods=["POST"])
def add_book():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        book = BookService.create_book(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if not book:
        return jsonify({"error": "Failed to create book"}), 400

    response = {
        "message": "Book added successfully",
        "book": book.to_dict()  # Correctly return the newly added book
    }
    return jsonify(response), 201


@book_bp.route("/books/<string:sku>", methods=["DELETE"])
def delete_book(sku):
    """
    Delete a book by SKU.
    """
    if not BookService.delete_book(sku):
        return jsonify({"error": "Book not found"}), 404

    response = {
        "message": f"Book with SKU {sku} deleted successfully",
        "books": [book.to_dict() for book in BookService.get_all_books()]
    }
    return jsonify(response), 200


@book_bp.route("/books/<string:sku>", methods=["PUT"])
def update_book(sku):
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        book = BookService.get_book_by_id(sku)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if not book:
        return jsonify({"error": "Book not found"}), 404

    try:
        book.update_book(data["title"], data["author"], data["publication_year"],
                         data["genre"], data["read_status"], data["rating"], data["notes"])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "Book updated successfully", "book": book.to_dict()}), 200


@book_bp.route("/books/stats", methods=["GET"])
def get_stats():
    stats = {
        "total_books": len(BookService.get_all_books()),
        "read_books": len([book for book in BookService.get_all_books() if book.read_status]),
        "unread_books": len([book for book in BookService.get_all_books() if not book.read_status]),
        "average_rating": sum(book.rating for book in BookService.get_all_books()) / len(BookService.get_all_books()) if BookService.get_all_books() else 0,
    }
    return jsonify(stats), 200
