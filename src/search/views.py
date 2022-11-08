# django base
from django.db import DatabaseError
from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

# add base
from time import sleep

# add our project
from .serializers import *

# Create your views here.
class SearchRequestViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = search_request.objects.all()
    serializer_class = SearchRequestSerializer
class SearchResultViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = search_result.objects.all()
    serializer_class = SearchResultSerializer

# # 검색방법
# maincategory_id를 입력한다
# 해당 서브랑 패턴을 하나씩 검색한다.
# 겹치는 것이 있다면, +1점을 한다.
# 그 다음 메인 서브 색상 점수를 기준으로 정렬한다.
# 이것은 완전히 겹치면 1점으로 한다.
# 그렇게 점수가 가장 높은 녀석부터 오름차순한다.

def test_rank_result(image_id, maincategory_id, t=1):
    # image_attributes에서 attribute 확인
    img_attr = ImageAttributesTable.objects.filter(image_id = image_id)
    # sub category 확인 추가
    # pattern 확인 추가
    # main color 확인
    # sub color 확인
    for attr in img_attr:
        print(attr, attr.attributes )
        target_attr = attr.attributes
        
    
    

