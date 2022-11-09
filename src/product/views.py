from django.shortcuts import render
from django.http import Http404

from rest_framework import generics, status
#from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from .models import *
from .serializer import *
from .permissions import IsOwnerOrReadOnly

# Create your views here.

#상품 등록 페이지 출력
class ProductViewSet(ModelViewSet):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, method=['GET'])
    def user_product_list(self, request):
        user_product_set = Product.objects.filter(seller=self.request.user)
        return Response(self.serializer_class(user_product_set, many=True).data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

product_register = ProductViewSet.as_view({
    'post': 'create',
})

product_list = ProductViewSet.as_view({
    'get': 'list',
})

product_detail = ProductViewSet.as_view({
    'get': 'retrieve',
})

user_product_list = ProductViewSet.as_view({
    'get': 'user_product_list',
})