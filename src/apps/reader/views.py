import logging
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.books.models import Book
from .models import ReadingList, BookStatus, ReaderProfile
from .forms import ReaderRegistrationForm, UserAuthenticationForm, ReadingListForm


def logout_page(request):
    """Logs out the user and redirects to the home page."""
    logout(request)
    return redirect('/')


def login_page(request):
    """Handles user login. If authenticated, redirects to home page; otherwise, renders login form."""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        form = UserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('home:home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = UserAuthenticationForm()
    return render(request, 'auth/login.html', context={'form': form})


def register(request):
    """Handles user registration. On successful registration, logs in the user."""
    if request.method == "POST":
        form = ReaderRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home:home")
        else:
            for error in form.errors:
                messages.error(request, form.errors[error].as_text())

    form = ReaderRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})


@login_required
def reading_list_view(request):
    """Displays the user's reading list, excluding archived entries."""
    archived_status = get_object_or_404(BookStatus, name="archived")
    readings = ReadingList.objects.filter(reader__user=request.user).exclude(status=archived_status)
    return render(request, 'pages/reading_list.html', {'readings': readings, 'statuses': BookStatus.objects.all().distinct()})


@login_required
def add_to_reading_view(request):
    """Adds a book to the user's reading list with the status 'Started'."""
    if request.method == 'POST':
        book_uid = request.POST.get('book_uid')
        book = get_object_or_404(Book, uid=book_uid)
        print(book)
        reader_profile = get_object_or_404(ReaderProfile, user=request.user)

        if ReadingList.objects.filter(reader=reader_profile, book=book).exists():
            return JsonResponse({
                'status': 'error',
                'message': f"'{book.title}' is already in your reading list."
            })

        status, _ = BookStatus.objects.get_or_create(name="started") 
        ReadingList.objects.create(reader=reader_profile, book=book, status=status)

        return JsonResponse({
            'status': 'success',
            'message': f"'{book.title}' added to your reading list with status 'Started'."
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def update_reading_view(request):
    """Updates the status of a book in the user's reading list."""
    if request.method == 'POST':
        reading_list_id = request.POST.get('reading_id')
        new_status_name = request.POST.get('status')
        
        reading_list_entry = get_object_or_404(ReadingList, id=reading_list_id)
        new_status, _ = BookStatus.objects.get_or_create(name=new_status_name)

        reading_list_entry.status = new_status
        reading_list_entry.save()

        return JsonResponse({
            'status': 'success',
            'message': f"Reading status updated to '{new_status.name}'."
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def remove_from_reading_view(request, uid):
    """Removes a book from the user's reading list."""
    entry = get_object_or_404(ReadingList, uid=uid, reader__user=request.user)
    entry.delete()
    return redirect('reader:reading_list')
