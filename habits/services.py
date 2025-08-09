from django.utils import timezone
from datetime import timedelta

from django.core.mail import send_mail
from django.db.models import Q

import requests
from django.conf import settings
from .models import Habit


def send_telegram_message(chat_id, message):
    params = {
        "text": message,
        "chat_id": chat_id,
    }
    print(chat_id)
    requests.post(f"{settings.TELEGRAM_URL}{settings.TELEGRAM_BOT_TOKEN}/sendMessage", params=params)


def get_habits_to_process():
    """
    Returns list of habits that need to be processed
    :return: 
    """
    today = timezone.now().date()

    # Условия для разных типов периодичности
    daily_condition = Q(periodicity="daily") & ~Q(updated_at__date=today)
    weekly_condition = Q(periodicity="weekly") & Q(updated_at__date__lte=today - timedelta(days=7))
    monthly_condition = Q(periodicity="monthly") & Q(updated_at__date__lte=today - timedelta(days=30))

    # Единый запрос к БД
    habits = Habit.objects.filter(
        is_active=True, is_enjoyable=False
    ).filter(
        daily_condition | weekly_condition | monthly_condition
    ).select_related("user")
    return habits


def message_for_habit(habit):
    user = habit.user
    activity = habit.activity
    time = habit.time.strftime('%H:%M')
    reward = (
        habit.related_habit.activity
        if habit.related_habit
        else habit.reward or "no reward specified"
    )
    message = (f"Hi {user.email} !\n "
               f"You have new habits to do {activity} at {time}.\n "
               f"Reward for doing this activity is {reward}")
    title = "Habit reminder"
    try:
        if user.tg_chat_id:
            send_telegram_message(user.tg_chat_id, message)
        send_mail(
            title,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send notification: {e}")

