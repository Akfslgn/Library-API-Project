from db import book_data


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

    # Optional fields (no validation errors if missing)
    if "read_status" in data and not data["read_status"]:
        error["read_status"] = "Read status cannot be empty if provided."
    if "rating" in data and not isinstance(data["rating"], (int, float)):
        error["rating"] = "Rating must be a number if provided."
    if "notes" in data and not isinstance(data["notes"], str):
        error["notes"] = "Notes must be a string if provided."

        # Check for duplicate SKU
    if data.get("sku") and any(book.sku == data["sku"] for book in book_data):
        error["sku"] = "A book with this SKU already exists."

        # Check if SKU is alphanumeric
    if data.get("sku") and not data["sku"].isalnum():
        error["sku"] = "SKU must be alphanumeric."
        # Check if title is a string
    if data.get("title") and not isinstance(data["title"], str):
        error["title"] = "Title must be a string."
        # Check if author is a string
    if data.get("author") and not isinstance(data["author"], str):
        error["author"] = "Author must be a string."
        # Check if genre is a string
    if data.get("genre") and not isinstance(data["genre"], str):
        error["genre"] = "Genre must be a string."
        # Check if publication year is a number
    if data.get("publication_year") and not isinstance(data["publication_year"], int):
        error["publication_year"] = "Publication year must be a number."
        # Check if read status is a string
    if data.get("read_status") and not isinstance(data["read_status"], str):
        error["read_status"] = "Read status must be a string."
        # Check if rating is a number
    if data.get("rating") and not isinstance(data["rating"], (int, float)):
        error["rating"] = "Rating must be a number."
        # Check if notes is a string
    if data.get("notes") and not isinstance(data["notes"], str):
        error["notes"] = "Notes must be a string."
    # Check for duplicate title
    if data.get("title") and any(book.title == data["title"] for book in book_data):
        error["title"] = "A book with this title already exists."

    return len(error) == 0, error
