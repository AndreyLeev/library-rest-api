from datetime import date

from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework.test import APIClient, APIRequestFactory
from django.contrib.auth.models import User
from django.urls import reverse

from library import views
from library.serializers import BookSerializer, UserSerializer
from library.models import Book


class ViewsTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        #Create 25 User objects
        number_of_users = 25
        for i in range(number_of_users):
            #Create 3 Book objects for each test_user
            test_user = User.objects.create_user(username='testuser'+str(i), password='password')
            number_of_books = 3
            for j in range(number_of_books):
                Book.objects.create(title='title'+str(j)+'usr'+str(i),
                                    author='test_author',
                                    description='test_desc',
                                    borrowed=test_user,
                                    pub_date=date.today(),
                                    age_limit=0) 
       
    def test_pages_paginated(self):
        """Confirm that only 20 items are displayed due to pagination
            (if pagination not enabled, there would be 25 returned)"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data.get('results')), 20)

    def test_get_valid_all_user(self):
        for test_user in User.objects.all():
            url = reverse('user-detail', kwargs={'username': test_user.username})
            response = self.client.get(url)
            self.assertEqual(response.data['id'], UserSerializer(test_user).data['id'])
            self.assertEqual(response.data['username'], UserSerializer(test_user).data['username'])
    
    def test_valid_user_self_links(self):
        for test_user in User.objects.all():
            url = reverse('user-detail', kwargs={'username': test_user.username})
            response = self.client.get(url)
            self_link = response.data.get('links').get('self') 
            response = self.client.get(self_link)
            self.assertEqual(response.data['id'], UserSerializer(test_user).data['id'])         
            

    def test_valid_user_books_links(self):
        for test_user in User.objects.all():
            url = reverse('user-detail', kwargs={'username': test_user.username})
            response = self.client.get(url)
            books_link = response.data.get('links').get('books')
            self_link = response.data.get('links').get('self') 
            response = self.client.get(books_link)
            for book in response.data.get('results'):
                borrowed_link = book.get('links').get('borrowed')
                self.assertEqual(borrowed_link, self_link)

    def test_create_valid_user(self):
        valid_payload = {
            'username': 'valid_user',
            'password': 'valid_password',
        }
        url = reverse('user-list')
        response = self.client.post(url, valid_payload)
        self.assertEqual(response.status_code, 201)

    def test_create_invalid_user(self):
        valid_payload = {
            'username': 'invalid_user,!',
            'password': 'valid_password',
        }
        url = reverse('user-list')
        response = self.client.post(url, valid_payload)
        self.assertEqual(response.status_code, 400)

    def test_create_valid_book(self):
        valid_payload = {
            'title':'test_title',
            'author':'test_author',
            'description':'test_desc',
            'pub_date':date.today(),
            'age_limit':0,
        }
        for test_user in User.objects.all():
            url = reverse('book-list', kwargs={'username': test_user.username})
            response = self.client.post(url, valid_payload)
            self.assertEqual(response.status_code, 201)
    
    def test_create_invalid_book(self):
        invalid_payload = {
            'title':'test_title',
            'author':'test_author',
            'description':'test_desc',
            'pub_date': date.today(),
            'age_limit':-12, #invalid
        }
        for test_user in User.objects.all():
            url = reverse('book-list', kwargs={'username': test_user.username})
            response = self.client.post(url, invalid_payload)
            self.assertEqual(response.status_code, 400)
    
    def test_modify_books_for_user(self):
        valid_payload = {
            'title':'test_title',
            'author':'test_author',
            'description':'test_desc',
            'pub_date': date.today(),
            'age_limit':0,
        } 
        test_user = User.objects.all()[0]
        url = reverse('user-detail', kwargs={'username': test_user.username})
        response = self.client.get(url)
        books_link = response.data.get('links').get('books') 
        response = self.client.get(books_link)
        for book in response.data.get('results'): 
            book_id = book.get('id')     
            url = reverse('book-detail', kwargs={'username': test_user.username, 'pk': book_id})
            response = self.client.put(url, valid_payload)
            self.assertEqual(response.status_code, 200)
    
