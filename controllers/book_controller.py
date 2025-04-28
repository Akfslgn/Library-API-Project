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
        return jsonify({"error": "Payload cannot be empty"}), 400

    try:
        books = BookService.create_book(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if not books or not isinstance(books, list):
        return jsonify({"error": "Unexpected error occurred while creating the book"}), 500

    response = {
        "message": "Book created successfully",
        "books": [book.to_dict() for book in books]
    }
    return jsonify(response), 201


@book_bp.route("/books/<string:sku>", methods=["DELETE"])
def delete_book(sku):
    """
    Delete a book by SKU.
    """
    try:
        deleted, books = BookService.delete_book(sku)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

    response = {
        "message": f"Book with SKU {sku} deleted successfully",
        "books": [book.to_dict() for book in books]
    }
    return jsonify(response), 200


@book_bp.route("/books/<string:sku>", methods=["PUT"])
def update_book(sku):
    """
    Update a book by SKU.
    """
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        updated, books = BookService.update_book(sku, data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

    response = {
        "message": f"Book with SKU {sku} updated successfully",
        "books": [book.to_dict() for book in books]
    }
    return jsonify(response), 200


@book_bp.route("/books/stats", methods=["GET"])
def get_stats():
    stats = {
        "total_books": len(BookService.get_all_books()),
        "read_books": len([book for book in BookService.get_all_books() if book.read_status]),
        "unread_books": len([book for book in BookService.get_all_books() if not book.read_status]),
        "average_rating": sum(book.rating for book in BookService.get_all_books()) / len(BookService.get_all_books()) if BookService.get_all_books() else 0,
    }
    return jsonify(stats), 200
