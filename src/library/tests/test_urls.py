from datetime import date  

from django.urls import include, path, reverse, resolve
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework.test import APIClient

from library import views
from library.models import Book


class UrlsTests(APITestCase):

    def setUp(self):
        self.factory = APIClient()
        self.test_user = User.objects.create_user(username='testuser', password='password')
        self.test_book = Book.objects.create(title='test_title',
                                            author='test_author',
                                            description='test_desc',
                                            borrowed=self.test_user,
                                            pub_date=date.today(),
                                            age_limit=0)

    def test_user_url_resolves(self):
        url = reverse('user-list')
        self.assertEquals(resolve(url).func.cls, views.UserView)
        url = reverse('user-detail', kwargs={'username': 'testuser1'})
        self.assertEquals(resolve(url).func.cls, views.UserView)
    
    def test_book_list_for_boorowed_url_resolves(self):
        url = reverse('book-list', kwargs={'username': 'testuser1'})
        self.assertEquals(resolve(url).func.cls, views.BookListView)

    def test_book_detail_for_boorowed_url_resolves(self):
        url = reverse('book-detail',
                    kwargs={'username': 'testuser1', 'pk':1})
        self.assertEquals(resolve(url).func.cls, views.BookDetailView)

    def test_user_list_view_url_accessible(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_user_detail_view_url_accessible(self):
        url = reverse('user-detail', kwargs={'username': self.test_user.username})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_nonexistent_user_detail_view_url(self):
        url = reverse('user-detail', kwargs={'username': 'nonexistent_user'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_book_list_view_url_accessible(self):
        url = reverse('book-list', kwargs={'username': self.test_user.username})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_book_detail_view_url_accessible(self):
        url = reverse('book-detail', kwargs={'username': self.test_user.username,
                                             'pk': self.test_book.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    
    def test_nonexistent_book_detail_view_url(self):
        url = reverse('book-detail', kwargs={'username': self.test_user.username,
                                             'pk': 123})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    