from repositories.book_repository import BookRepository


def validate_book_data(data):
    error = {}

    # Mandatory fields
    if not data.get("sku"):
        error["sku"] = "SKU is required."
    if not data.get("title"):
        error["title"] = "Title is required."
    if not data.get("author"):
        error["author"] = "Author is required."
    if not data.get("publication_year"):
        error["publication_year"] = "Publication year is required."
    if not data.get("genre"):
        error["genre"] = "Genre is required."

    # Optional fields
    if "read_status" in data and not isinstance(data["read_status"], str):
        error["read_status"] = "Read status must be a string."
    if "rating" in data and data["rating"] is not None and not isinstance(data["rating"], (int, float)):
        error["rating"] = "Rating must be a number between 0 and 5."
    if "notes" in data and data["notes"] is not None and not isinstance(data["notes"], str):
        error["notes"] = "Notes must be a string."

    # Check for duplicate SKU
    if data.get("sku"):
        existing_book = BookRepository.get_book_by_id(data["sku"])
        if existing_book:
            error["sku"] = "A book with this SKU already exists."

    if data.get("title"):
        existing_book = BookRepository.get_book_by_title(data["title"])
        if existing_book:
            error["title"] = "A book with this title already exists."

    return error if error else None
