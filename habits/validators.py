from .models import Habit
from rest_framework.exceptions import ValidationError


def validate_habit(attrs):
    related_habit = attrs.get("related_habit")
    reward = attrs.get("reward")
    time = attrs.get("time_to_complete")
    enjoyable = attrs.get("is_enjoyable")
    period = attrs.get("periodicity")

    valid_periods = [choice[0] for choice in Habit._meta.get_field('periodicity').choices]

    if related_habit is not None and reward:
        raise ValidationError("Нельзя указывать одновременно связанную привычку и вознаграждение!")
    elif related_habit is not None:
        if enjoyable:
            raise ValidationError("Приятная привычка не должна быть связанной с другой привычкой!")
        related_habit_obj = Habit.objects.filter(id=related_habit.id).first()
        if related_habit_obj and not related_habit_obj.is_enjoyable:
            raise ValidationError("Связанная привычка должна быть приятной!")
    elif enjoyable and (reward is not None or related_habit is not None):
        raise ValidationError("Для приятной привычки нельзя указывать вознаграждение или связанную привычку!")
    elif time and time > 120:
        raise ValidationError("Время выполнения привычки не должно превышать 2 часа!")
    elif period is not None and period not in valid_periods:
        raise ValidationError(f"Неверная периодичность! Возможные периодичности: {', '.join(valid_periods)}")
    return attrs
