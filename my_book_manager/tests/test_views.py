from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch
from my_book_manager.models import SearchHistory, Book, Favorite, Comment

# Use get_user_model to get the custom user model
CustomUser = get_user_model()


class HomeViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass'
        )
        self.client.login(email='test@example.com', password='testpass')

    @patch('requests.get')
    def test_home_view_with_query(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'items': [{'id': '123', 'volumeInfo': {'title': 'Test Book'}}]
        }

        response = self.client.get(reverse('home'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        self.assertIn('search_history', response.context)

    def test_home_view_without_query(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/home.html')
        self.assertIn('search_history', response.context)


class BookDetailViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass'
        )
        self.client.login(email='test@example.com', password='testpass')
        self.book = Book.objects.create(google_book_id='test-id')

    @patch('requests.get')
    def test_book_detail_view(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'id': 'test-id',
            'volumeInfo': {'title': 'Test Book'}
        }

        response = self.client.get(reverse('book_detail', args=['test-id']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')

    @patch('requests.get')
    def test_add_favorite(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'id': 'test-id',
            'volumeInfo': {'title': 'Test Book'}
        }

        self.client.post(reverse('book_detail', args=['test-id']), {'add_favorite': True})
        self.assertTrue(Favorite.objects.filter(user=self.user, book=self.book).exists())

    @patch('requests.get')
    def test_remove_favorite(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'id': 'test-id',
            'volumeInfo': {'title': 'Test Book'}
        }

        self.client.post(reverse('book_detail', args=['test-id']), {'add_favorite': True})
        self.client.post(reverse('book_detail', args=['test-id']), {'remove_favorite': True})
        self.assertFalse(Favorite.objects.filter(user=self.user, book=self.book).exists())


class AddCommentViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass'
        )
        self.client.login(email='test@example.com', password='testpass')
        self.book = Book.objects.create(google_book_id='test-id')

    def test_add_comment(self):
        response = self.client.post(reverse('add_comment', args=['test-id']), {'content': 'Great book!'})
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertTrue(Comment.objects.filter(user=self.user, book=self.book, content='Great book!').exists())


class FavoritesViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass'
        )
        self.client.login(email='test@example.com', password='testpass')

    def test_favorites_view(self):
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/favorites.html')


class SearchHistoryViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass'
        )
        self.client.login(email='test@example.com', password='testpass')

    def test_search_history_view(self):
        response = self.client.get(reverse('search_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/search_history.html')
