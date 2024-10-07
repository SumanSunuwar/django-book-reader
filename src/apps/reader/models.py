from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from apps.books.models import Book, Genre
from apps.common.models import BaseTimestampModel

class ReaderProfile(BaseTimestampModel):
    """
    Model representing a reader profile.
    
    Attributes:
        user (ForeignKey): Links to the built-in User model.
        favorite_genre (ForeignKey): User's favorite genre.
        reading_list (ManyToManyField): A list of selected books (Book) the reader has added.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="reader_profile")
    favorite_genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)  
    reading_list = models.ManyToManyField(Book, related_name='readers', blank=True)

    class Meta:
        verbose_name = "Reader Profile"
        verbose_name_plural = "Reader Profiles"

    def __str__(self):
        """Return a string representation of the reader."""
        return self.user.username
    
    def clean(self):
        """Custom validation to ensure favorite_genre exists."""
        if self.favorite_genre is not None and not Genre.objects.filter(id=self.favorite_genre.id).exists():
            raise ValidationError("The selected favorite genre does not exist.")


class BookStatus(BaseTimestampModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Book Status"
        verbose_name_plural = "Book Status"

    def __str__(self):
        return f"Status: {self.name}"


class ReadingList(BaseTimestampModel):
    reader = models.ForeignKey(ReaderProfile, on_delete=models.CASCADE, related_name='reading_entries')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_list_entries')
    status = models.ForeignKey(BookStatus, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('reader', 'book')

    def __str__(self):
        return f"{self.reader.user.username}'s reading list: {self.book.title} - Status: {self.status}"

    def get_reading_list(self):
        """Return all books in the reading list with their statuses."""
        return [
            {
                'book': entry.book,
                'status': entry.status,
                'added_on': entry.added_on,
            }
            for entry in self.reading_entries.all()
        ]