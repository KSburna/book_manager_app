import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import CustomAuthUserCreationForm, CustomAuthUserLoginForm, UserDetailsForm
from .models import Book, SearchHistory, Favorite, Comment

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"


# Home view with search functionality
@login_required
def home_view(request):
    query = request.GET.get("q")
    books = []

    # Fetch latest 5 searches for the user
    latest_searches = SearchHistory.objects.filter(user=request.user).order_by(
        "-viewed_at"
    )[:5]

    if query:
        response = requests.get(GOOGLE_BOOKS_API_URL, params={"q": query})
        if response.status_code == 200:
            data = response.json()
            books = data.get("items", [])

    if query is None:
        query = ""
    context = {"books": books, "query": query, "search_history": latest_searches}
    return render(request, "book/home.html", context)


# Book detail view
@login_required
def book_detail(request, google_book_id):
    # Fetch book details from Google Books API
    response = requests.get(f"{GOOGLE_BOOKS_API_URL}/{google_book_id}")
    book_data = response.json() if response.status_code == 200 else None

    # Initialize the favorite status
    is_favorite = False

    if book_data:
        book, created = Book.objects.get_or_create(google_book_id=google_book_id)
        # Add to SearchHistory if the book is viewed
        SearchHistory.objects.get_or_create(user=request.user, book=book)

        # Check if the book is a favorite
        is_favorite = Favorite.objects.filter(user=request.user, book=book).exists()

        # Handle adding/removing from favorites
        if request.method == "POST":
            if "add_favorite" in request.POST:
                Favorite.objects.get_or_create(user=request.user, book=book)
                is_favorite = True
            elif "remove_favorite" in request.POST:
                is_favorite = False
                Favorite.objects.filter(user=request.user, book=book).delete()

        # Fetch comments for this book
        comments = Comment.objects.filter(book=book)

    context = {
        "book_data": book_data,
        "google_book_id": google_book_id,
        "is_favorite": is_favorite,
        "comments": comments,
    }
    return render(request, "book/book_detail.html", context)


# View for user's search history
@login_required
def search_history(request):
    user_history = SearchHistory.objects.filter(user=request.user).select_related(
        "book"
    )
    context = {"search_history": user_history}
    return render(request, "book/search_history.html", context)


# View for user's favorite books
@login_required
def favorites(request):
    user_favorites = Favorite.objects.filter(user=request.user).select_related("book")
    context = {"favorites": user_favorites}
    return render(request, "book/favorites.html", context)


@login_required
def add_comment(request, google_book_id):
    if request.method == "POST":
        book = get_object_or_404(Book, google_book_id=google_book_id)
        content = request.POST.get("content")

        if content:
            Comment.objects.create(user=request.user, book=book, content=content)
        else:
            print("no comment")

    return redirect("book_detail", google_book_id=google_book_id)


def signup_view(request):
    if request.method == "POST":
        form = CustomAuthUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("home")
    else:
        form = CustomAuthUserCreationForm()
    return render(request, "book/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = CustomAuthUserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("home")
    else:
        form = CustomAuthUserLoginForm()
    return render(request, "book/login.html", {"form": form})


@login_required
def change_user_details(request):
    user = request.user
    if request.method == "POST":
        form = UserDetailsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UserDetailsForm(instance=user)

    return render(request, "book/change_user_details.html", {"form": form})
