from django.shortcuts import render
from .serializer import UserSerializer
from .models import User
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# Create your views here.

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

def logout(request):
    auth.logout(request)
    return redirect('home')