from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.serializers import RegisterSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
