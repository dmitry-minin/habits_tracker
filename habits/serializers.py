from rest_framework import serializers
from .models import Habit
from habits.validators import validate_habit
from rest_framework.fields import TimeField


class HabitSerializer(serializers.ModelSerializer):
    """
    Serializer for Habit model
    """
    time = TimeField(format="%H:%M", input_formats=["%H:%M"])

    class Meta:
        model = Habit
        fields = [
            "id",
            "place",
            "time",
            "activity",
            "is_enjoyable",
            "related_habit",
            "periodicity",
            "reward",
            "time_to_complete",
            "is_public",
            "is_active",
        ]
        extra_kwargs = {
            "user": {"write_only": True},
            "id": {"read_only": True}
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return validate_habit(attrs)


class PublicHabitSerializer(serializers.ModelSerializer):
    """
    Serializer for Habit model when information about public habits is needed
    """
    time = TimeField(format="%H:%M", input_formats=["%H:%M"])

    class Meta:
        model = Habit
        fields = [
            "user",
            "place",
            "time",
            "activity",
            "is_enjoyable",
            "related_habit",
            "periodicity",
            "reward",
            "time_to_complete"
        ]
        read_only_fields = fields
        ordering = ["user"]
