from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOwner

from users.models import User
from users.serializers import UserSerializer


class UserCreateView(CreateAPIView):
    """
    Create a new user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]


class UserRetrieveView(RetrieveAPIView):
    """
    Retrieve a user data
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwner,)


class UserUpdateView(UpdateAPIView):
    """
    Update a user data
    Don't allow to update password
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwner,)

    def perform_update(self, serializer):
        serializer.validated_data.pop("password", None)
        super().perform_update(serializer)


class UserDeleteView(DestroyAPIView):
    """
    Delete a user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwner,)
