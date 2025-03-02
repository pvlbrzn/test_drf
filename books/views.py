from rest_framework import generics
from .models import Book
from .serializers import BookSerializer


# Методы GET + POST
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# Получение, обновление и удаление одной книги (GET, PUT, DELETE)
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
