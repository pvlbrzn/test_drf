import os
import requests
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Book
from dotenv import load_dotenv


# Функция для отправки сообщений в Telegram
def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.get(url, params=params)
    return response


load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


# Сигнал, который срабатывает после сохранения объекта в базе данных
@receiver(post_save, sender=Book)
def notify_on_create(sender, instance, created, **kwargs):
    if created:  # Проверяем, что объект был только что создан
        message = f"Новая книга добавлена в базу: {instance.title, instance.author}"
        send_telegram_message(TOKEN, CHAT_ID, message)


# Сигнал, который срабатывает перед удалением объекта из базы данных
@receiver(pre_delete, sender=Book)
def notify_on_delete(sender, instance, **kwargs):
    message = f"Книга была удалена: {instance.title, instance.author}"
    send_telegram_message(TOKEN, CHAT_ID, message)


@receiver(post_save, sender=Book)
def send_notification_email(sender, instance, created, **kwargs):
    if created:  # Если запись только что создана
        subject = "📚 Новая книга добавлена!"
        message = f"Добавлена новая книга:\n\nНазвание: {instance.title}\nАвтор: {instance.author}\nГод: {instance.year}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [settings.EMAIL_HOST_USER]  # Отправляем уведомление себе
        send_mail(subject, message, from_email, recipient_list)
