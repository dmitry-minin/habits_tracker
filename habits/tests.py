from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from users.models import User
from habits.models import Habit


class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", password="password")
        self.habit = Habit.objects.create(
            user=self.user,
            place="test place",
            time="12:00",
            activity="test activity",
            is_enjoyable=False,
            periodicity="daily",
            reward="test reward",
            time_to_complete=60,
            is_public=True,
        )
        self.client.force_authenticate(user=self.user)


    def test_retrieve_habit(self):
        url = reverse("habits:habits-detail", args=[self.habit.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["place"], self.habit.place)
        self.assertEqual(response.data["time"], self.habit.time)
        self.assertEqual(response.data["activity"], self.habit.activity)
        self.assertEqual(response.data["is_enjoyable"], self.habit.is_enjoyable)
        self.assertEqual(response.data["related_habit"], None)
        self.assertEqual(response.data["periodicity"], self.habit.periodicity)
        self.assertEqual(response.data["reward"], self.habit.reward)
        self.assertEqual(response.data["time_to_complete"], self.habit.time_to_complete)
        self.assertEqual(response.data["is_public"], self.habit.is_public)
        self.assertEqual(response.data["is_active"], self.habit.is_active)

    def test_update_habit(self):
        url = reverse("habits:habits-detail", args=[self.habit.id])
        data = {
            "place": "new place",
            "time": "13:00",
            "activity": "new activity",
            "periodicity": "weekly",
            "reward": "new reward",
            "time_to_complete": 120,
            "is_public": False,
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.place, data["place"])
        self.assertEqual(self.habit.time.strftime("%H:%M"), data["time"])
        self.assertEqual(self.habit.activity, data["activity"])
        self.assertEqual(self.habit.periodicity, data["periodicity"])
        self.assertEqual(self.habit.reward, data["reward"])
        self.assertEqual(self.habit.time_to_complete, data["time_to_complete"])
        self.assertEqual(self.habit.is_public, data["is_public"])

    def test_list_habits(self):
        url = reverse("habits:habits-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        habit_data = response.data['results'][0]

        self.assertEqual(habit_data["place"], self.habit.place)
        self.assertEqual(habit_data["time"], self.habit.time)
        self.assertEqual(habit_data["activity"], self.habit.activity)
        self.assertEqual(habit_data["is_enjoyable"], self.habit.is_enjoyable)
        self.assertEqual(habit_data["periodicity"], self.habit.periodicity)
        self.assertEqual(habit_data["reward"], self.habit.reward)
        self.assertEqual(habit_data["time_to_complete"], self.habit.time_to_complete)
        self.assertEqual(habit_data["is_public"], self.habit.is_public)
        self.assertEqual(habit_data["is_active"], self.habit.is_active)

    def test_create_habit(self):
        url = reverse("habits:habits-list")
        data = {
            "user": self.user.id,
            "place": "new place create",
            "time": "13:00",
            "activity": "new activity create",
            "is_enjoyable": True,
            "periodicity": "monthly",
            "time_to_complete": 20,
            "is_public": False,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)
        self.assertEqual(response.data["place"], data["place"])
        self.assertEqual(response.data["time"], data["time"])
        self.assertEqual(response.data["activity"], data["activity"])
        self.assertEqual(response.data["is_enjoyable"], data["is_enjoyable"])
        self.assertEqual(response.data["periodicity"], data["periodicity"])
        self.assertEqual(response.data["time_to_complete"], data["time_to_complete"])
        self.assertEqual(response.data["is_public"], data["is_public"])

    def test_retrieve_public_habits(self):
        url = reverse("habits:habits-public")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_habit(self):
        url = reverse("habits:habits-detail", args=[self.habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

