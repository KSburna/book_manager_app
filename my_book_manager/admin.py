from django.contrib import admin
from .models import Book, SearchHistory, Favorite, Comment


# Custom admin for the Book model, displaying dynamically fetched info
class BookAdmin(admin.ModelAdmin):
    list_display = ('google_book_id', 'get_title', 'get_authors', 'get_published_date')
    search_fields = ['google_book_id']

    def get_title(self, obj):
        details = obj.get_book_details()
        return details.get('volumeInfo', {}).get('title', 'N/A') if details else 'N/A'
    get_title.short_description = 'Title'

    def get_authors(self, obj):
        details = obj.get_book_details()
        authors = details.get('volumeInfo', {}).get('authors', [])
        return ', '.join(authors) if authors else 'N/A'
    get_authors.short_description = 'Authors'

    def get_published_date(self, obj):
        details = obj.get_book_details()
        return details.get('volumeInfo', {}).get('publishedDate', 'N/A') if details else 'N/A'
    get_published_date.short_description = 'Published Date'


# Admin for tracking search history, similar to favorites
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_book_title', 'viewed_at')
    list_filter = ('user', 'viewed_at')

    def get_book_title(self, obj):
        details = obj.book.get_book_details()
        return details.get('volumeInfo', {}).get('title', 'N/A') if details else 'N/A'
    get_book_title.short_description = 'Book Title'


# Admin for managing favorites
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_book_title', 'added_at')
    list_filter = ('user', 'added_at')

    def get_book_title(self, obj):
        details = obj.book.get_book_details()
        return details.get('volumeInfo', {}).get('title', 'N/A') if details else 'N/A'
    get_book_title.short_description = 'Book Title'


# Admin for managing comments on books
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_book_title', 'content', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ['content', 'user__email']

    def get_book_title(self, obj):
        details = obj.book.get_book_details()
        return details.get('volumeInfo', {}).get('title', 'N/A') if details else 'N/A'
    get_book_title.short_description = 'Book Title'


# Registering the models to admin site
admin.site.register(Book, BookAdmin)
admin.site.register(SearchHistory, SearchHistoryAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Comment, CommentAdmin)
