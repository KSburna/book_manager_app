import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import CustomAuthUserCreationForm, CustomAuthUserLoginForm, UserDetailsForm
from .models import Book, SearchHistory

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"


# Home view with search functionality
@login_required
def home_view(request):
    query = request.GET.get("q")
    books = []

    if query:
        response = requests.get(GOOGLE_BOOKS_API_URL, params={"q": query})
        if response.status_code == 200:
            data = response.json()
            books = data.get("items", [])

    if query is None:
        query = ""
    context = {"books": books, "query": query}
    return render(request, "book/home.html", context)


# Book detail view
@login_required
def book_detail(request, google_book_id):
    # Fetch book details from Google Books API
    response = requests.get(f"{GOOGLE_BOOKS_API_URL}/{google_book_id}")
    book_data = response.json() if response.status_code == 200 else None

    if book_data:
        book, created = Book.objects.get_or_create(google_book_id=google_book_id)
        # Add to SearchHistory if the book is viewed
        SearchHistory.objects.get_or_create(user=request.user, book=book)

    context = {"book_data": book_data, "google_book_id": google_book_id}
    return render(request, "book/book_detail.html", context)


# View for user's search history
@login_required
def search_history(request):
    user_history = SearchHistory.objects.filter(user=request.user).select_related(
        "book"
    )
    context = {"search_history": user_history}
    return render(request, "book/search_history.html", context)


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
