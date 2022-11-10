from abc import *
from pickle import NONE

from random import randrange
import time
import sys

# set path
import sys
from pathlib import Path
import os

FASHION_BASE_DIR=Path(__file__).resolve().parent.parent.parent
tmp = FASHION_BASE_DIR
if str(tmp) not in sys.path and os.path.isabs(tmp):
    sys.path.append(str(tmp))  # add ROOT to PATH
from analysis.models import image_attributes
from label.models import Attributes
from detect_utills import PipeResource, copy_piperesource, is_test
from pipe_cls import IPipeObserver, One2OnePipe
def is_test_pipe_utills()->bool:
    return True and is_test()

def test_print(s, s1="", s2="", s3="", s4="", s5="", end="\n"):
    if is_test_pipe_utills():
        print("pipe cls exe : ", s, s1, s2, s3, s4, s5, end=end)

test_print("FASHION_BASE_DIR :",FASHION_BASE_DIR)

 
def search_label_attributes_class(type_id, name) -> int:
    attr = Attributes.objects.get(type_id=type_id, data__class=name)
    return attr.id

class ImageCropPipe(One2OnePipe):
    def __init__(self) -> None:
        super().__init__()
    
    def exe(self, input: PipeResource) -> PipeResource:#output
        #첫번째 det를 기준으로 im을 크롭해서 im를 교환해 주는 그런 파이프
        # 첫번째 det 선택
        det= input.dets[0]
        im = input.im
        #crop
        crop_img = im[det["ymin"]:det["ymax"],det["xmin"]:det["xmax"]]
        #change im
        input.images["croped"] = crop_img
        input.im = crop_img
        return input
    
    def get_regist_type(self, idx=0) -> str:
        return "img-crop"

class SaveAttributesClassPipe(IPipeObserver):
    def __init__(self, display=False) -> None:
        super().__init__()
        self.src=None
        self.display = display
    
    def push_src(self, input: PipeResource) -> None:
        self.src = input
        image_id = input.metadata["img_id"]
        obj_idx = input.metadata["obj_id"]
        attr_name = input.metadata["attributes_name"]
        attr_type = input.metadata["type_id"]
        attribute_id = search_label_attributes_class(attr_type, attr_name)
        attr = image_attributes(image_id=image_id, obj_idx=obj_idx, attribute_id=attribute_id)
        try:
            attr.save()
            print(f"({attr_type}){attr_name} success!")
        except:
            if self.display:
                print(f"({attr_type}){attr_name} fail")
    
    def print(self):
        if self.src is not None:
            self.src.print()
    
    