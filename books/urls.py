from django.urls import path, include
from .views import BookListCreateView, BookDetailView
from rest_framework_swagger.views import get_swagger_view
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('api/books/', BookListCreateView.as_view(), name='book-list'),
    path('api/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs')
]
