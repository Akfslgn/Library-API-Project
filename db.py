from models.book_model import Book

Book1 = Book(
    sku="001",
    title="The Great Gatsby",
    author="F. Scott Fitzgerald",
    publication_year=1925,
    genre="Fiction",
    read_status="Read",
    rating=4.5,
    notes="A classic novel set in the 1920s."
)
Book2 = Book(
    sku="002",
    title="To Kill a Mockingbird",
    author="Harper Lee",
    publication_year=1960,
    genre="Fiction",
    read_status="Not Read",
    rating=4.2,
    notes="A classic novel about racial injustice in the South."
)


book_data = [Book1, Book2]
