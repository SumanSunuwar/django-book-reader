from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Author, Book, Genre


def home(request):
    """
    View for rendering the homepage with a list of genres.
    """
    genres = Genre.objects.all()
    context = {'genres': genres}
    return render(request, 'pages/home.html', context)


class BookListView(ListView):
    """
    List view for displaying all books with pagination.
    """
    model = Book
    template_name = 'pages/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        """
        Customize the queryset to order books by title.
        """
        return Book.objects.all().order_by('title')


class BookDetailView(DetailView):
    """
    Detail view for displaying detailed information about a book.
    """
    model = Book
    template_name = 'pages/book_detail.html'
    context_object_name = 'book'

    def get_object(self):
        """
        Fetch a book by its 'uid' from the URL instead of the primary key.
        """
        uid = self.kwargs.get('uid')
        return get_object_or_404(Book, uid=uid)

    def get_context_data(self, **kwargs):
        """
        Add additional context for authors and related books based on genres.
        """
        context = super().get_context_data(**kwargs)
        book = self.object

        if book.authors.exists():
            context['primary_author'] = book.authors.first()
            context['other_authors'] = book.authors.exclude(uid=context['primary_author'].uid)
        else:
            context['primary_author'] = None
            context['other_authors'] = []

        context['related_books'] = Book.objects.filter(genres__in=book.genres.all()).exclude(uid=book.uid).distinct()
        return context


class AuthorListView(ListView):
    """
    List view for displaying all authors with pagination.
    """
    model = Author
    template_name = 'pages/author.html'
    context_object_name = 'authors'
    paginate_by = 10

    def get_queryset(self):
        """
        Customize the queryset to order authors by their first name.
        """
        return Author.objects.all().order_by('first_name')


class AuthorDetailView(DetailView):
    """
    Detail view for displaying detailed information about an author.
    """
    model = Author
    template_name = 'author_detail.html'
    context_object_name = 'author'

    def get_object(self):
        """
        Fetch an author by its 'uid' from the URL instead of the primary key.
        """
        uid = self.kwargs.get('uid')
        return get_object_or_404(Author, uid=uid)

    def get_context_data(self, **kwargs):
        """
        Add additional context to display books written by the author.
        """
        context = super().get_context_data(**kwargs)
        author = self.object

        if author.books.exists():
            context['books'] = author.books
        return context


class AuthorFilterView(ListView):
    """
    List view to filter books by a specific author.
    """
    model = Book
    template_name = 'pages/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        """
        Filter the books by the specified author's UID.
        """
        author_uid = self.kwargs['author_uid']
        return Book.objects.filter(authors__uid=author_uid).distinct()

    def get_context_data(self, **kwargs):
        """
        Add the author's information to the context.
        """
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(Author, uid=self.kwargs['author_uid'])
        context['author'] = author
        return context


class GenreFilterView(ListView):
    """
    List view to filter books by a specific genre.
    """
    model = Book
    template_name = 'pages/book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        """
        Filter the books by the specified genre's UID.
        """
        genre_uid = self.kwargs['genre_uid']
        return Book.objects.filter(genres__uid=genre_uid).distinct()


class GenreListView(ListView):
    """
    List view for displaying all genres and their associated books.
    """
    model = Book
    template_name = 'pages/genre.html'
    context_object_name = 'books'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        """
        Add all genres to the context.
        """
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        return context

    def get_queryset(self):
        """
        Filter books by genre if a genre UID is provided.
        """
        genre_uid = self.kwargs.get('uid')

        if genre_uid:
            genre = get_object_or_404(Genre, uid=genre_uid)
            return Book.objects.filter(genres=genre)
        
        return Book.objects.all()


def search_books(request):
    """
    Handle search functionality for books by title, author, or genre.
    """
    query = None
    books = []
    selected_filter = None
    no_results_message = ""

    if request.method == 'POST':
        selected_filter = request.POST.get('filter')
        query = request.POST.get('search_query')

        if query:
            query = query.strip()

            if len(query) < 3:
                messages.error(request, "Search input must be at least 3 characters long.")
            else:
                if selected_filter == 'By Genre':
                    books = Book.objects.filter(Q(genres__name__icontains=query)).distinct()
                    if not books.exists():
                        no_results_message = "No books found for this genre."
                        messages.error(request, no_results_message)

                elif selected_filter == 'By Author':
                    name_parts = query.split()
                    author_filter = Q(authors__first_name__icontains=name_parts[0]) | Q(authors__last_name__icontains=name_parts[-1])

                    if len(name_parts) == 3:
                        author_filter |= Q(authors__middle_name__icontains=name_parts[1])

                    books = Book.objects.filter(author_filter).distinct()
                    if not books.exists():
                        no_results_message = "No books found for this author."
                        messages.error(request, no_results_message)

                elif selected_filter == 'By Title':
                    books = Book.objects.filter(title__icontains=query).distinct()
                    if not books.exists():
                        messages.error(request, "No books found with this title.")
                else:
                    books = Book.objects.filter(title__icontains=query).distinct()
                    if not books.exists():
                        messages.error(request, "No books found with this title.")
        else:
            messages.error(request, "Please enter a search query.")

    return render(request, 'pages/book_search.html', {
        'books': books,
        'query': query,
        'selected_filter': selected_filter,
    })
