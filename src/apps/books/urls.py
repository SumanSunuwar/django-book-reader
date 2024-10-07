from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/<uuid:uid>/', views.BookDetailView.as_view(), name='book_detail'),

    path('books/genres/', views.GenreListView.as_view(), name='genre_list'),
    path('books/genre/<uuid:uid>/', views.GenreListView.as_view(), name='book_by_genre'),

    path('books/author/<uuid:author_uid>/', views.AuthorFilterView.as_view(), name='filter_by_author'),

    path('books/authors', views.AuthorListView.as_view(), name='author_list'),
    path('author/<uuid:author_uid>/', views.AuthorDetailView.as_view(), name='author_detail'),


    path('search/', views.search_books, name='search_books'),

]