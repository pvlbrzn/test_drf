from django.urls import path, include
from .views import BookListCreateView, BookDetailView

urlpatterns = [
    path('api/books/', BookListCreateView.as_view(), name='book-list'),
    path('api/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
]
