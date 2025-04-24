from flask import Flask, render_template, request, jsonify
from controllers.book_controller import book_bp
from services.book_service import BookService


def create_app():
    app = Flask(__name__)
    # Enable CORS for all routes
    app.register_blueprint(book_bp)

    @app.route("/")
    def home():
        books = BookService.get_all_books()
        stats = calculate_stats(books)
        print("Books:", books)
        print("Stats:", stats)
        return render_template("index.html", books=books, stats=stats)

    def calculate_stats(books):
        if not books:
            return None
        total_books = len(books)
        books_read = sum(
            1 for book in books if book.read_status.lower() == 'read')
        books_not_read = total_books - books_read
        average_rating = sum(book.rating for book in books) / total_books
        most_popular_genre = max(
            set(book.genre for book in books),
            key=lambda g: sum(1 for book in books if book.genre == g)
        )
        highest_rated_book = max(books, key=lambda book: book.rating)
        most_recent_book = max(books, key=lambda book: book.created_at)
        return {
            "total_books": total_books,
            "books_read": books_read,
            "books_not_read": books_not_read,
            "average_rating": average_rating,
            "most_popular_genre": most_popular_genre,
            "highest_rated_book": highest_rated_book,
            "most_recent_book": most_recent_book
        }

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": "Bad Request",
            "message": getattr(error, "description", "Invalid request.")
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Not Found",
            "message": getattr(error, "description", "Resource not found.")
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "error": "Internal Server Error",
            "message": getattr(error, "description", "An unexpected error occurred.")
        }), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
