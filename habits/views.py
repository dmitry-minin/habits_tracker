from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import HabitSerializer, PublicHabitSerializer
from .models import Habit
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsOwner


class HabitViewSet(ModelViewSet):
    """
    API endpoint that allows habits to be viewed or edited.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy", "retrieve"]:
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(user=self.request.user)
        return self.queryset

    @action(detail=False, methods=["get"])
    def public(self, request):
        """
        Shows all public habits
        """

        habits = Habit.objects.filter(is_active=True, is_public=True,)
        if not habits.exists():
            return NotFound("No public habits found")
        serializer = PublicHabitSerializer(habits, many=True)
        return Response(serializer.data)
