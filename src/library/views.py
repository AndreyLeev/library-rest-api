from django.contrib.auth.models import User 
from rest_framework import viewsets, generics

from . import serializers
from .models import Book


class UserView(viewsets.ModelViewSet):
    """API endpoint for listing and creating users"""

    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class BookListView(generics.ListCreateAPIView):
    """API endpoint for listing and creating books"""

    serializer_class = serializers.BookSerializer

    def get_queryset(self):
        queryset = Book.objects.filter(borrowed__username=self.kwargs.get('username'))
        return queryset

    def perform_create(self, serializer):
        serializer.save(borrowed=User.objects.filter(username=self.kwargs.get('username'))[0])


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint for updating book"""
    
    serializer_class = serializers.BookSerializer
    queryset = Book.objects.all()
