from django.contrib.auth import authenticate, get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework import generics
from main.serializers import UserSerializer
User = get_user_model()


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def api_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'status': 'Ошибка: Введите пароль и логин'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'status': 'Ошибка: неправильные логин или пароль'},
                        status=HTTP_404_NOT_FOUND)
    return Response({'status': 'success'},
                    status=HTTP_200_OK)


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
