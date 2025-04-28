from uuid import uuid4
from datetime import datetime


class Book:
    def __init__(self, sku, title, author, publication_year, genre, read_status, rating, notes, uuid=None, created_at=None, **kwargs):
        self.sku = sku
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.genre = genre
        self.read_status = read_status
        self.rating = rating
        self.notes = notes
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = datetime.now()
        self.uuid = uuid if uuid else str(uuid4())

    def update_book(self, title, author, publication_year, genre, read_status, rating, notes):
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.genre = genre
        self.read_status = read_status
        self.rating = rating
        self.notes = notes
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "sku": self.sku,
            "title": self.title,
            "author": self.author,
            "publication_year": self.publication_year,
            "genre": self.genre,
            "read_status": self.read_status,
            "rating": self.rating,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "uuid": self.uuid,
        }
