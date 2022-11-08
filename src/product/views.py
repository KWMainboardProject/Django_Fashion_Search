from django.shortcuts import render
from django.http import Http404

from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import *
from .serializer import *
from .permissions import IsOwnerOrReadOnly

# Create your views here.

#상품 등록 페이지 출력
class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


# 사용자의 상품 리스트 출력
#class ProductList



# 상품 상세 페이지 출력
"""
class ProductDetail(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Product.objects.get(pk)
"""
