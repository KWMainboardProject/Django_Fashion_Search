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
class AnalysisStateSViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = pipe_work_state.objects.all()
    serializer_class = AnalysisStateSerializer
class ImageAttributesSViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = image_attributes.objects.all()
    serializer_class = ImageAttributesSerializer
 
 # state 검색기능도 제공해야 한다. image_id 를 기반으로 하는 검색을 말이다.
 # image_id를 기반으로 속성들을 모두 보여주는 기능이 필요하다.

def test_make_attributes(img_id, t=1):
    print("======== test ============")
    carom_img = carom.objects.get(id=img_id)
    carom_img.detect_state="P"
    carom_img.save()
    print("======== start Process ============")
    sleep(t*3)
    print("======== detect done ============")
    coord = balls_coord(carom_id=img_id, coord={"cue" : [200, 200], "obj1" : [600, 200], "obj2" : [200, 150]})
    coord.save()
    carom_img.detect_state="D"
    carom_img.save()
    print("======== save ball_coord ============")

# class DetectRequestAPIView(APIView):
#     def make_attributes(self, img_id):
#         import threading
#         #detect PIPE
#         try:
#             runner = threading.Thread(target=test_make_attributes, args=(img_id))
#             runner.start()
#         except Exception as ex:
#             print("make_coord ex : "+ str(ex))
    
#     def get(self, request, img_id, maincategory_id=None,format=None):
#         try:
#             print(f'maincategory : {maincategory_id}')
#         except:
#             pass
#         # image_id 존재하는지 확인
#         try:
#             img_obj = request_image.objects.get(img_id = img_id)
#         except request_image.DoesNotExist: # 이미지가 아직 저장 안된 경우
#             return Response({"message":"Image doesn't exist"},status=status.HTTP_404_NOT_FOUND)
        
#         # image의 state 확인
#         state = img_obj.analysis_state
        
        
#         if state == "P":
#             # 연산이 진행중일때, 
#             # pipe_work_state를 확인하여, 
#             # 연산 상황 확인하여 최신화 시켜준다.
#              return Response({"state":"Progress"}, status=status.HTTP_202_ACCEPTED) #기다리라고 한다.
        
#         elif state == "U":
#             # 연산이 시작하지 않았다면, 연산을 시작한다.
#             self.make_attributes(img_id)
#             return Response({"state":"Undefine"}, status=status.HTTP_202_ACCEPTED) #기다리라고 한다.
        
#         elif state == "D":
#             #연산이 끝났을 때, 값을 반환해 준다.
#             try:
                
                
                
                
                
#                 coord_obj = balls_coord.objects.get(carom_id=carom_id)
#                 http_status = status.HTTP_200_OK
#                 serializer = CoordSerializer(coord_obj)
#             except:
#                 return Response({"message":"Ball Corrdination doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
#             # requester 로그 쌓기
#             try:
#                 # request를 찾고
#                 requester = detect_request.objects.get(carom_id=carom_id, requester=usr)
#             except detect_request.DoesNotExist:
#                 #존재 하지 않으면 새로 생성
#                 detect_request(carom_id=carom_id, requester=usr).save()
#             return Response(serializer.data, status=http_status)
        
#         #진행중이라면
#         return Response({"state":"Progress"}, status=status.HTTP_202_ACCEPTED) #기다리라고 한다.