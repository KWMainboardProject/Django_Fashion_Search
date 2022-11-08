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
class ImageAttributesViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = image_attributes.objects.all()
    serializer_class = ImageAttributesSerializer
    
class ImageAttributesTableViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = ImageAttributesTable.objects.all()
    serializer_class = ImageAttributesTableSerializer
 
 # state 검색기능도 제공해야 한다. image_id 를 기반으로 하는 검색을 말이다.
 # image_id를 기반으로 속성들을 모두 보여주는 기능이 필요하다.

def test_make_attributes(img_id, t=1):
    print("======== test ============")
    detect_img = request_image.objects.get(id=img_id)
    detect_img.analysis_state="P"
    detect_img.save()
    print("======== start Process ============")
    sleep(t*3)
    print("======== detect done ============")
    image_attributes(image_id=img_id, attribute_id=23, obj_idx=1).save() # 반팔
    image_attributes(image_id=img_id, attribute_id=33, obj_idx=1).save() # 프린팅
    image_attributes(image_id=img_id, attribute_id=185, obj_idx=1).save() # 반팔
    image_attributes(image_id=img_id, attribute_id=211, obj_idx=1).save() # 반팔
    detect_img.analysis_state="D"
    detect_img.save()
    print("======== save attributes ============")

class DetectRequestAPIView(APIView):
    lookup_field = 'id'
    def make_attributes(self, img_id):
        import threading
        #detect PIPE
        try:
            runner = threading.Thread(target=test_make_attributes, args=(img_id, 1))
            runner.start()
        except Exception as ex:
            print("make_attributes ex : "+ str(ex))
    def get(self, request, img_id, maincategory_id=None,format=None):
        
        # image_id 존재하는지 확인
        try:
            img_obj = request_image.objects.get(id = img_id)
        except request_image.DoesNotExist: # 이미지가 아직 저장 안된 경우
            return Response({"message":"Image doesn't exist"},status=status.HTTP_404_NOT_FOUND)
        
        # image의 state 확인
        state = img_obj.analysis_state
        
        
        if state == "U":
            # 연산이 시작하지 않았다면, 연산을 시작한다.
            self.make_attributes(img_id)
            return Response({"state":"Undefine"}, status=status.HTTP_202_ACCEPTED) #기다리라고 한다.
        
        elif state == "D":
            #연산이 끝났을 때, 값을 반환해 준다.
            try:
                if maincategory_id is None:
                    result = ImageAttributesTable.objects.filter(image_id=img_id)
                else :
                    result = ImageAttributesTable.objects.filter(image_id=img_id, maincategory_id=maincategory_id)
                http_status = status.HTTP_200_OK
                serializer = ImageAttributesTableSerializer(result, many=True)
            except:
                return Response({"message":"Image doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data, status=http_status)
        
        #진행중이라면
        return Response({"state":"Progress"}, status=status.HTTP_202_ACCEPTED) #기다리라고 한다.