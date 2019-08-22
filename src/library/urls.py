from django.urls import path, include 
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('user', views.UserView)

urlpatterns = [
    path('', include(router.urls)),
    path('user/<str:username>/book/', views.BookListView.as_view(), name='book-list'),
    path('user/<str:username>/book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
]