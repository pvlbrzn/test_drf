from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class BookAPITestCase(APITestCase):

    def setUp(self):
        """Создаём тестового пользователя и авторизуем его"""
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)  # авторизация пользователя

    def test_create_book(self):
        """Тест создания книги"""
        data = {
            "title": "новая книга",
            "author": "новый автор",
            "description": "описание",
            "year": "2025"
        }
        response = self.client.post("/api/books/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Проверяем статус 201

    def test_get_books_list(self):
        """Тест получения списка книг"""
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверяем статус 200
        self.assertGreaterEqual(len(response.data), 1)  # Должна быть хотя бы одна книга
