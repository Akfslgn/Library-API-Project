from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

books = [
    {
        "book_id": "001",
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "publication_year": 1925,
        "genre": "Fiction",
        "read_status": "Read",
        "rating": 5.3,
        "notes": "A classic novel about the American dream.",
    },
    {
        "book_id": "002",
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "publication_year": 1960,
        "genre": "Fiction",
        "read_status": "Read",
        "rating": 4.9,
        "notes": "A classic novel about racial injustice in the South.",
    },
    {
        "book_id": "003",
        "title": "1984",
        "author": "George Orwell",
        "publication_year": 1949,
        "genre": "Dystopian",
        "read_status": "Not Read",
        "rating": 4.8,
        "notes": "A dystopian novel about a totalitarian society.",
    },
    {
        "book_id": "004",
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "publication_year": 1951,
        "genre": "Fiction",
        "read_status": "Read",
        "rating": 4.7,
        "notes": "A coming-of-age novel about a teenage boy's journey.",
    },
    {
        "book_id": "005",
        "title": "The Lord of the Rings",
        "author": "J.R.R. Tolkien",
        "publication_year": 1954,
        "genre": "Fantasy",
        "read_status": "Read",
        "rating": 4.9,
        "notes": "A classic novel about a quest to destroy the One Ring.",
    },

]


@app.route('/')
def index():
    return render_template('index.html', books=books)


@app.route("/api/books", methods=["GET"])
def get_books():
    return jsonify(books)


@app.route("/api/books/<string:book_id>", methods=["GET"])
def get_book(book_id):
    print(f"deta recieved: {book_id}")
    for book in books:
        if book["book_id"] == book_id:
            return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404


@app.route("/api/books", methods=["POST"])
def add_book():
    """
    request body:
    {
        "book_id": "006",
        "title": "New Book Title",
        "author": "Author Name",
        "publication_year": 2025,
        "genre": "Genre",
        "read_status": "Not Read",
        "rating": 4.5,
        "notes": "Some notes about the book."
    }
    """
    new_book = request.json

    if not new_book:
        return jsonify({"error": "Invalid request"}), 400

    if "title" not in new_book or "author" not in new_book:
        return jsonify({"error": "Missing required fields"}), 400

    if "book_id" not in new_book:
        return jsonify({"error": "Missing book_id"}), 400

    for book in books:
        if book["book_id"] == new_book["book_id"]:
            return jsonify({"error": "Book ID already exists"}), 400

    print(f"===== Type of book name: {type(new_book).__name__} =====")

    if type(new_book.get("title")).__name__ != "str":
        return jsonify({"error": "Title must be a string"}), 400

    books.append(new_book)
    # jsonify({"status": f"Book {new_book.get('title')} added successfully"}), 201
    return jsonify({"status": f"Book {new_book.get('title')} added successfully with id: {new_book.get('book_id')}", "books": books}), 201


@app.route("/api/books/<string:book_id>", methods=["PUT"])
def update_book(book_id):
    updated_book = request.json
    for book in books:
        if book["book_id"] == book_id:
            book.update(updated_book)
            return jsonify({"status": f"Book {book.get('title')} updated successfully", "books": books}), 200
    return jsonify({"error": "Book not found"}), 404


@app.route("/api/books/<string:book_id>", methods=["DELETE"])
def delete_book(book_id):
    for book in books:
        if book["book_id"] == book_id:
            books.remove(book)
            return jsonify({"status": f"Book {book.get('title')} deleted successfully"}), 200
    return jsonify({"error": "Book not found"}), 404


@app.route("/api/books/stats", methods=["GET"])
def get_books_stats():
    total_books = len(books)
    read_status_count = {"Read": 0, "Not Read": 0}
    genre_count = {}
    total_rating = 0
    rated_books_count = 0

    for book in books:
        # Count read status
        if book["read_status"] in read_status_count:
            read_status_count[book["read_status"]] += 1

        # Count genres
        genre = book["genre"]
        if genre in genre_count:
            genre_count[genre] += 1
        else:
            genre_count[genre] = 1

        # Calculate average rating
        if "rating" in book and isinstance(book["rating"], (int, float)):
            total_rating += book["rating"]
            rated_books_count += 1

    average_rating = total_rating / rated_books_count if rated_books_count > 0 else 0

    stats = {
        "total_books": total_books,
        "read_status_count": read_status_count,
        "average_rating": round(average_rating, 2),
        "books_count_by_genre": genre_count,
    }

    return jsonify(stats), 200


if __name__ == '__main__':
    app.run(debug=True)
