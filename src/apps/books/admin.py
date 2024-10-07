from django.contrib import admin
from .models import Author, Genre, Book, BookAuthor, Publisher

class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        obj.save(user=request.user)
        super().save_model(request, obj, form, change)  # Call the parent method


# Inline model for BookAuthor to handle the Many-to-Many relationship between Book and Author
class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1
    autocomplete_fields = ['author']  # To help with large author lists
    ordering = ('order',)

# Admin for Author with Books Inline
class AuthorAdmin(BaseAdmin, admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'image')
    search_fields = ('first_name', 'middle_name', 'last_name', 'bio')
    ordering = ('last_name', 'first_name')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')  # Make these fields read-only
    inlines = [BookAuthorInline]  # Inline to show books written by this author

# Admin for Genre with self-referential relationships handling sub-genres
class GenreAdmin(BaseAdmin, admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('parent',)  # Filter by parent genre to manage sub-genres
    autocomplete_fields = ['parent']  # Autocomplete for parent genre

# Admin for Publisher with inline Book representation
class PublisherAdmin(BaseAdmin, admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    #inlines = [BookAuthorInline]  # Show books from the publisher

# Admin for Book with Author inline and genre filter
class BookAdmin(BaseAdmin, admin.ModelAdmin):
    list_display = ('title', 'get_authors', 'isbn', 'publication_date', 'publisher')
    search_fields = ('title', 'isbn', 'authors__first_name', 'authors__last_name', 'publisher__name')
    list_filter = ('genres', 'publication_date', 'publisher')
    ordering = ('title',)
    autocomplete_fields = ['publisher', 'authors', 'genres']  # Auto complete for related fields
    inlines = [BookAuthorInline]  # Show authors inline within book admin

    # Function to display authors
    def get_authors(self, obj):
        return ", ".join([str(author) for author in obj.authors.all()])
    get_authors.short_description = 'Authors'

# Admin for BookAuthor to control the order of authors in the book
class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ('book', 'author', 'order')
    search_fields = ('book__title', 'author__first_name', 'author__last_name')
    list_filter = ('book', 'author')
    ordering = ('book', 'order')

# Registering models and the enhanced admin views
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
