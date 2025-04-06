from django.contrib import admin
from django.contrib import messages
from .models import Book
from reports import send_excel_report


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "year")

    actions = ["send_report_email"]

    def send_report_email(self, request, queryset):
        """Отправляет отчет с книгами по email"""
        send_excel_report()
        self.message_user(request, "📧 Отчет отправлен на почту!", messages.SUCCESS)

    send_report_email.short_description = "📨 Отправить отчет по email"
