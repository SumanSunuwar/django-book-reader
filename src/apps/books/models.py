from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.books.helper import author_image_upload_path, book_cover_upload_path, genre_cover_upload_path
from apps.common.models import BaseTimestampModel
import uuid

# Helper function to generate unique upload paths for images
def upload_to(instance, filename):
    return f'{instance.__class__.__name__.lower()}_images/{uuid.uuid4()}-{filename}'

class Author(BaseTimestampModel):
    """
    Model representing an author.
    
    Attributes:
        first_name (str): The author's first name.
        middle_name (str): The author's middle name (optional).
        last_name (str): The author's last name.
        bio (str): A brief biography of the author (optional).
        comments (str): Any additional comments or notes about the author (optional).
        image (ImageField): A profile image of the author.
    """
    first_name = models.CharField(_('First name'), max_length=255)
    last_name = models.CharField(_('Last name'), max_length=255)
    middle_name = models.CharField(_('Middle name'), max_length=255, null=True, blank=True, default=None)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=author_image_upload_path, blank=True, null=True)

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")
        ordering = ['last_name', 'first_name']

    def __str__(self) -> str:
        return f"{self.first_name} {self.middle_name or ''} {self.last_name}".strip()


class Publisher(BaseTimestampModel):
    """
    A model representing a publisher.
    
    Attributes:
        name (str): The name of the publisher.
    """
    name = models.CharField(_('Publisher name'), max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Publisher")
        verbose_name_plural = _("Publishers")
        ordering = ['name']


class Genre(BaseTimestampModel):
    """
    Model representing a genre, which can have a parent genre (sub-genre relationship).
    
    Attributes:
        name (str): The name of the genre.
        parent (ForeignKey): Self-referential FK for sub-genres.
    """
    name = models.CharField(_('Genre'), max_length=100, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subgenres', on_delete=models.SET_NULL)
    genre_image = models.ImageField(upload_to=genre_cover_upload_path, blank=True, null=True)
    # is_root = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    # def save(self, *args, **kwargs):
    #     # Automatically set is_root if parent is None
    #     if self.parent is None:
    #         self.is_root = True
    #     else:
    #         self.is_root = False
    #     super().save(*args, **kwargs)


class Book(BaseTimestampModel):
    """
    Model representing a book in the library.

    Attributes:
        title (str): The title of the book.
        isbn (str): ISBN for the book.
        num_pages (int): Number of pages in the book.
        publisher (ForeignKey): The publisher of the book.
        authors (ManyToManyField): Authors of the book.
        genres (ManyToManyField): Genres of the book.
        publication_date (DateField): The publication date of the book.
        summary (TextField): A brief summary of the book.
        cover_image (ImageField): The cover image for the book.
    """
    title = models.CharField(_('Book Title'), max_length=255, unique=True)
    isbn = models.CharField(_('ISBN'), max_length=16, null=True, blank=True, default=None)
    isbn13 = models.CharField(_('ISBN-13'), max_length=16, null=True, blank=True, default=None)
    num_pages = models.PositiveIntegerField(_('Num Pages'), null=True, blank=True, default=None)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books', null=True)
    authors = models.ManyToManyField(Author, verbose_name=_('Authors'), related_name='books', through='BookAuthor')
    genres = models.ManyToManyField(Genre, related_name='books', blank=True)
    year_published = models.IntegerField(_('Year Published'), null=True, blank=True, default=None)
    original_publication_year = models.IntegerField(_('Original Publication Year'), null=True, blank=True, default=None)
    publication_date = models.DateField(_('Publication Date'), blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to=book_cover_upload_path, blank=True, null=True)

    @property
    def primary_author(self) -> Author:
        """Return the top-billed author for this book."""
        return self.authors.get(bookauthor__order=1)

    @property
    def other_authors(self) -> "models.QuerySet[Author]":
        """Return all authors other than the top-billed author."""
        return self.authors.filter(bookauthor__order__gt=1)

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
        ordering = ['title']

    def __str__(self) -> str:
        return self.title


class BookAuthor(models.Model):
    """
    Through table between Book and Author to maintain the order of authorship.
    
    Attributes:
        book (ForeignKey): Reference to the Book.
        author (ForeignKey): Reference to the Author.
        order (int): Order of the author in the book's author list.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_('Author'))
    order = models.PositiveIntegerField(_('Author order'), default=1)

    class Meta:
        unique_together = ('book', 'author', 'order')
        verbose_name = _("Book Author")
        verbose_name_plural = _("Book Authors")
        ordering = ('book', 'order')
