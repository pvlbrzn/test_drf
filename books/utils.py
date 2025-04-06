from django.conf import settings
from celery import shared_task
from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import Book


@shared_task
def send_pdf_report():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    y_position = 730
    for book in Book.objects.all():
        c.drawString(100, y_position, f"Title: {book.title}. Author: {book.author}. Year: {book.year}")
        y_position -= 20
    c.save()

    buffer.seek(0)
    subject = "Это не СКАМ, честно)"
    message = "Фишинг сообщения от Паши, открывай обязательно"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ["nemez.09.pop@gmail.com"]

    email = EmailMessage(
        subject,
        message,
        from_email,
        recipient_list
    )
    email.attach("report.pdf", buffer.read(), "application/pdf")
    email.send(fail_silently=False)

