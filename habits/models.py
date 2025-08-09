from django.db import models
from conf.settings import AUTH_USER_MODEL


class Habit(models.Model):
    choices = (
        ("daily", " ежедневно"),
        ("weekly", " еженедельно"),
        ("monthly", " ежемесячно"),
    )
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Owner", help_text="Owner")
    place = models.CharField(max_length=100, verbose_name="Place", help_text="Place where you want to do this habit")
    time = models.TimeField(verbose_name="Time", help_text="Time when you want to do this habit in format HH:MM")
    activity = models.CharField(max_length=100, verbose_name="Activity",
                                help_text="Activity you want to do")
    is_enjoyable = models.BooleanField(null=True, verbose_name="Enjoyable habit",
                                       help_text="Is this habit enjoyable True/False")
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                                      verbose_name="Related habit",
                                      help_text="Related habit, only for useful habits")
    periodicity = models.CharField(choices=choices, default="daily", max_length=20, verbose_name="Periodicity",
                                   help_text="How often you want to do this activity")
    reward = models.CharField(max_length=100, blank=True, null=True, verbose_name="Reward",
                              help_text="Reward for doing this activity")
    time_to_complete = models.PositiveIntegerField(verbose_name="Time to complete",
                                                   help_text="Time to complete this activity")
    is_public = models.BooleanField(default=True, blank=True, null=True, verbose_name="Public habit",
                                    help_text="Do you want to make this habit public")
    is_active = models.BooleanField(default=True, blank=True, null=True, verbose_name="Active habit",
                                    help_text="Active or not")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Habit"
        verbose_name_plural = "Habits"
        ordering = ["user"]

    def __str__(self):
        return self.activity
