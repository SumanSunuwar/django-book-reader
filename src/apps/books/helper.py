from uuid import uuid4
import os

def author_image_upload_path(instance, filename):
    """Generates a unique path for author images."""
    ext = filename.split('.')[-1]
    return os.path.join('authors', f"{instance.last_name}_{uuid4()}.{ext}")

def book_cover_upload_path(instance, filename):
    """Generates a unique path for book cover images."""
    ext = filename.split('.')[-1]
    return os.path.join('books', f"{instance.title}_{uuid4()}.{ext}")

def genre_cover_upload_path(instance, filename):
    """Generates a unique path for book cover images."""
    ext = filename.split('.')[-1]
    return os.path.join('genre', f"{instance.name}_{uuid4()}.{ext}")
