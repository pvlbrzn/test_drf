import os
from openpyxl import Workbook
from django.contrib import admin
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Book


@admin.action(description="📩 Отправить отчет (Excel) на email")
def send_books_report(modeladmin, request, queryset):
    """Создает Excel-отчет и отправляет его на email"""

    file_path = generate_excel_report()
    file_name = "books_report.xlsx"

    # Отправляем email
    subject = "📊 Отчет по книгам"
    message = "Во вложении Excel-отчет со списком книг."
    email = settings.EMAIL_HOST_USER  # Куда отправлять

    email_message = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])

    with open(file_path, "rb") as file:
        email_message.attach(file_name, file.read(),
                             "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    email_message.send()

    # Уведомление в админке
    modeladmin.message_user(request, "📧 Excel-отчет отправлен на почту!")


# Функция для создания Excel-отчета
def generate_excel_report():
    """Создает отчет в формате Excel"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Books Report"

    # Добавляем заголовки
    ws.append(["Title", "Author", "Year"])

    # Добавляем данные
    for book in Book.objects.all():
        ws.append([book.title, book.author, book.year])

    # Сохраняем файл в память
    file_path = os.path.join(settings.MEDIA_ROOT, "books_report.xlsx")
    wb.save(file_path)

    return file_path


# Регистрируем модель с кастомным действием
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "year")
    actions = [send_books_report]  # Добавляем кнопку в админку