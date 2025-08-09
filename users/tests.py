from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class UserTestCase(APITestCase):
    """
    Testing user endpoints
    """
    def setUp(self) -> None:
        self.user = User.objects.create_user(email="test@test.com", password="password", tg_chat_id="123")
        self.client.force_authenticate(user=self.user)

    def test_login_return_token(self):
        """
        Check login return token
        """
        url = reverse("users:login")
        response = self.client.post(
            url,
            {
                "email": "test@test.com",
                "password": "password"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        refresh = RefreshToken(response.data["refresh"])
        self.assertEqual(int(refresh["user_id"]), self.user.id)

    def test_refresh_token(self):
        """
        Check refresh token
        """
        login_url = reverse("users:login")
        login_response = self.client.post(
            login_url,
            {
                "email": "test@test.com",
                "password": "password"  # Пароль из setUp
            },
            format="json"
        )
        refresh_token = login_response.data["refresh"]

        refresh_url = reverse("users:token_refresh")
        response = self.client.post(
            refresh_url,
            {
                "refresh": refresh_token
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

        self.assertNotEqual(
            login_response.data["access"],
            response.data["access"]
        )


def test_retrieve_user(self):
    """
    Check retrieve user
    """
    url = reverse("users:user_retrieve", args=[self.user.id])
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data["email"], "test@test.com")
    self.assertEqual(response.data["tg_chat_id"], "123")


def test_update_user(self):
    """
    Check update user
    """
    url = reverse("users:user_update", args=[self.user.id])
    response = self.client.patch(
        url,
        {
            "email": "test1@test.com",
            "tg_chat_id": "321"
        },
        format="json"
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data["email"], "test1@test.com")
    self.assertEqual(response.data["tg_chat_id"], "321")


def test_create_user(self):
    """
    Check create user
    """
    url = reverse("users:user_create")
    response = self.client.post(
        url,
        {
            "email": "test2@test.com",
            "password": "testpassword123"
        },
        format="json"
    )
    print(response.data)  # Выведем ответ сервера
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data["email"], "test2@test.com")
    self.assertEqual(response.data["tg_chat_id"], None)
    self.assertEqual(User.objects.count(), 2)


def test_delete_user(self):
    """
    Check delete user
    """
    url = reverse("users:user_delete", args=[self.user.id])
    response = self.client.delete(url)
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(User.objects.count(), 0)
