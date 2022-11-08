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
    # 검색 진행중으로 변경
    request = search_request.objects.get(image_id=image_id, maincategory_id=maincategory_id)
    request.state = "P"
    request.save()
    
    request_id = request.image
    print("request ID : ", request_id)
    
    # image_attributes에서 attribute 확인
    img_attr = ImageAttributesTable.objects.filter(image_id = image_id)
    # sub category 확인 추가
    # pattern 확인 추가
    # main color 확인
    # sub color 확인
    for attr in img_attr:
        print("Image Attributes : ", attr, attr.attributes)
        # 특정 속성 추출
        target_attr = attr.attributes
        # 타겟 속성으로 검색
        product_attributes_list = ProductAttributes.objects.filter(attribute_id = target_attr)
        
        for product_attribute in product_attributes_list:
            print("Product : ", product_attribute, product_attribute.product)
            # 제품이 검색_결과로 존재하는지 확인
            product_id = product_attribute.product
            try :
                result = search_result.objects.get(product_id = product_id, request_id=request_id)
            except search_request.DoesNotExist:
            #   제품이 없다면, 새로 만든다.
                search_result(product_id = product_id, request_id=request_id, score=1.0)
                continue
            
            #   제품이 있다면, socore를 올린다.
            try:
                result.score = result.score + 1.0
                result.save
            except Exception as ex:
                print("Error : ", str(ex))
        
        # color 관련 거리계산
        
    # 검색 완료
    request.state = "D"
    request.save()
        
            
class SearchRequestAPIView(APIView):
    lookup_field = 'id'
    def make_result(self, image_id, maincategory_id):
        import threading
        try:
            runner = threading.Thread(target=test_rank_result, args=(image_id, maincategory_id))
            runner.start()
        except Exception as ex:
            print("make_result ex : ", str(ex))
    def get(self, request, img_id, maincategory_id, format=None):
        # 이미지 있나 확인
        try:
            img_obj = request_image.objects.get(id = img_id)
        except request_image.DoesNotExist: # 이미지가 아직 저장 안된 경우
            return Response({"message":"Image doesn't exist"},status=status.HTTP_404_NOT_FOUND)
        
        # search request 있나 확인
        try:
            request_obj = search_request.objects.get(image=img_obj, maincategory_id=maincategory_id)
        except search_request.DoesNotExist:
            # 없으면 만든다.
            request_obj = search_request(image_id = img_id, maincategory_id=maincategory_id)
            request_obj.save()
        # search requset state 확인
        state = request_obj.state
        
        if state == "U":
            # 연산이 시작하지 않았다면, 연산을 시작한다.
            self.make_result(img_id, maincategory_id)
            return Response({"state":"Undefine"}, status=status.HTTP_202_ACCEPTED) #기다리라고 한다.
        
        elif state == "D":
            #연산이 끝났을 때, 값을 반환해 준다.
            try:
                result_list = search_result.objects.filter(request=request_obj)
                http_status = status.HTTP_200_OK
                serializer = SearchResultSerializer(result_list, many=True)
            except Exception as ex :
                print("Search Result ex : ", str(ex))
                return Response({"message":"Request doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data, status=http_status)
        
        # 진행중이라면
        return Response({"state":"Progress"}, status=status.HTTP_202_ACCEPTED) #기다리라고 한다.
