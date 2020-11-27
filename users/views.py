from decouple import config
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterAPISerializer, LoginSerializer
from .send_mail import send_confirmation_email

User = get_user_model()

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterAPISerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                send_confirmation_email(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



class ActivationView(View):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return render(request, 'index.html', {})
        except User.DoesNotExist:
            return render(request, 'link_exp.html', {})


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer
