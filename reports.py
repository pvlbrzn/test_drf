import openpyxl
from io import BytesIO
from books.models import Book
from django.core.mail import EmailMessage
from django.conf import settings


def get_books_dict():
    queryset = Book.objects.all()
    books_dict = {book.title: {"author": book.author,
                               "year": book.year,
                               "description": book.description}
                  for book in queryset}
    return books_dict


def generate_excel_report():
    books_dict = get_books_dict()
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Список книг"
    # Заголовки
    headers = ["Название", "Автор", "Год", "Описание"]
    sheet.append(headers)
    for title, book in books_dict.items():
        sheet.append([title, book.get("author", ""), book.get("year", ""), book.get("description", "")])

    # Сохраняем в байтовый поток
    excel_stream = BytesIO()
    workbook.save(excel_stream)
    excel_stream.seek(0)

    return excel_stream


def send_excel_report():
    excel_file = generate_excel_report()

    # Состав письма
    subject = 'Отчет по книгам'
    message = 'Прикрепленный файл содержит отчет о книгах'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [settings.EMAIL_HOST_USER]  # Отправляем себе

    # Создаем письмо
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.attach("books_report.xlsx", excel_file.getvalue(),
                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Отправляем письмо
    email.send()
