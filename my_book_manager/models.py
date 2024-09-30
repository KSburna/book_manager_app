from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils import timezone
import requests

from my_book_manager import settings


class Book(models.Model):
    google_book_id = models.CharField(max_length=100, unique=True)  # Store the Google Book API ID

    class Meta:
        db_table = 'book'
        ordering = ['google_book_id']

    def __str__(self):
        return self.google_book_id

    # Method to fetch book details from Google Books API
    def get_book_details(self):
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes/{self.google_book_id}')
        if response.status_code == 200:
            return response.json()  # Returns full book details
        return None


# Model to track search history of the user
# Model to track search history of the user when they view a book
class SearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='search_history', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='searched_by', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'search_history'
        unique_together = ('user', 'book')  # Prevent duplicate entries for the same book in history

    def __str__(self):
        return f"{self.user.email} viewed {self.book.google_book_id}"


# Model to store favorite books of the user
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='favorites', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='favorited_by', on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'favorite'
        unique_together = ('user', 'book')  # Prevent duplicate favorites for the same book

    def __str__(self):
        return f"{self.user.email} favorited {self.book.title}"


# Model to store comments on books by users
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'comment'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} commented on {self.book.title}: {self.content[:50]}"


class CustomAuthUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomAuthUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomAuthUserManager()

    def __str__(self):
        return self.email
