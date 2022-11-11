import argparse
import time

import torch
from torch.nn import functional
from torchvision.transforms.functional import to_pil_image
from torchvision import transforms
from PIL import Image
import cv2
import numpy as np

# set path
import sys
from pathlib import Path
import os

FILE = Path(__file__).resolve()
ROOT = FILE.parent
tmp = ROOT / "yolov5"
if str(tmp) not in sys.path and os.path.isabs(tmp):
    sys.path.append(str(tmp))  # add ROOT to PATH

WEIGHT_DIR = None
FASHION_BASE_DIR=Path(__file__).resolve().parent.parent.parent
tmp = FASHION_BASE_DIR / 'weights'
if str(tmp) not in sys.path and os.path.isabs(tmp):
    WEIGHT_DIR= (tmp)  # add Weights ROOT to PATH

# import my project
from Singleton import Singleton
from pipe_cls import One2OnePipe, SplitMaincategory, ResourceBag
from model_weights import IWeight
from detect_utills import (PipeResource, LoadImages,
                           make_padding_image, copy_piperesource,
                           LOGGER, is_test, time_sync,
                           Annotator, colors, save_one_box)
def is_test_classfication()->bool:
    return True and is_test()

def test_print(s, s1="", s2="", s3="", s4="", s5="", end="\n"):
    if is_test_classfication():
        print("classfication pipe test : ", s, s1, s2, s3, s4, s5, end=end)

############################
from threading import Lock
from abc import *

#이미지 전처리 함수
def img_transform(img, imgsz=(224, 224)):
    test_print("img_transform" ,type(img))
    
    pre_transforms = transforms.Compose([
        transforms.Resize(imgsz),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    img = Image.fromarray(img)
    pre_img = pre_transforms(img)
    return pre_img

class ClassificationPipe(One2OnePipe):
    def __init__(self, model:IWeight) -> None:
        super().__init__()
        self.display = model.display
        
        self.name = model.NAME
        self.cls = model.cls
        self.attribute_type_id = model.ATTRBUTES_TYPE_ID
        self.conf_thres = model.conf_thres
        self.imgsz = model.imgsz
        self.lock = model.lock
        self.device = model.device
        self.model = model.model
    
    @torch.no_grad()
    def exe(self,
            input: PipeResource,
            visualize = False,
            agnostic_nms = False,
            classes = None
            ) -> PipeResource:
        t1 = time.time()

        # 고정 값
        device = self.device
        model = self.model
        imgsz = self.imgsz
        dt, seen = [0.0, 0.0, 0.0, 0.0], 0

        conf_thres = self.conf_thres
        # Preprocess
        t1 = time_sync()
        #   이미지 변환, 이미지 디바이스로 올리고
        im = input.im
        # im = img_transform(img=input.im, imgsz=imgsz)
        im =torch.from_numpy(im)
        im = img_transform(img=input.im, imgsz=imgsz)
        im = im.to(device)
        
        t2 = time_sync()
        dt[0] += t2 - t1
        # Inference
        with self.lock:
            output = model(im[None, ...])
            probs = torch.nn.functional.softmax(output, dim=1)
            conf, preds = torch.max(probs, 1)
            test_print(preds[0], len(self.cls))
            test_print(self.cls[preds[0]])
            result = self.cls[preds[0]]
            test_print("result) ", result)
        t3 = time_sync()
        dt[1] += t3 - t2
        # Postprocess
        input.metadata["type_id"] = self.attribute_type_id
        input.metadata["attributes_name"] = result
        input.metadata["attributes_index"] = preds[0]
        input.metadata["attributes_data_type"] = 1 #class
        if self.display:
            input.print()
        return input

    def get_regist_type(self, idx=0) -> str:
        return self.name
        

def test(src, device, display=True):
    from model_weights import TopSubcategoryClassficationWeight
    # from DetectObjectPipe import DetectObjectPipe
    
    ### Pipe 생성###
    top_sub_cls_pipe = ClassificationPipe(TopSubcategoryClassficationWeight(device=device, display=display))
    bag_split = ResourceBag()
    
    # 파이프 연결
    top_sub_cls_pipe.connect_pipe(bag_split)
    ### Dataloader ###
    dataset = LoadImages(src)
    ### 실행 ###
    for im0, path, s in dataset:
        metadata = {"path": path}
        images = {"origin":im0}
        input = PipeResource(im=im0, metadata=metadata, images=images, s=s)
        top_sub_cls_pipe.push_src(input)
    if display:
        for obj in bag_split.src_list:
            obj.imshow(metadata=["type_id", "attributes_name", "attributes_index"] ,hide_box=True)
            cv2.waitKey(0)
    else:
        bag_split.print()

def runner(args):
    test(args.src, args.device, args.display)
    #runascapp(args.src, args.device)
    #test_singleton()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', default= (FASHION_BASE_DIR / "media" / "test"))
    parser.add_argument('--device', default='0', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--display', action="store_true")
    args = parser.parse_args()
    print(args)
    runner(args) 