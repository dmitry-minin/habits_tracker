from celery import shared_task
from habits.services import get_habits_to_process, message_for_habit


@shared_task
def send_email_about_birthday():
    """
    Sends notification about habits, that need to be processed.
    For each habit sends notification through email and tg_channel if tg_channel is set
    """
    habits = get_habits_to_process()

    for habit in habits:
        message_for_habit(habit)






