import torch
import numpy as np
import argparse
import cv2
from PIL import Image 

# set path
import os
from pathlib import Path
import sys

FILE = Path(__file__).resolve()
ROOT = FILE.parent

tmp = ROOT
if str(tmp) not in sys.path and os.path.isabs(tmp):
    sys.path.append(str(tmp))  # add ROOT to PATH

tmp = ROOT / "yolov5"
if str(tmp) not in sys.path and os.path.isabs(tmp):
    sys.path.append(str(tmp))  # add ROOT to PATH

FASHION_BASE_DIR=Path(__file__).resolve().parent.parent.parent
tmp = FASHION_BASE_DIR
if str(tmp) not in sys.path and os.path.isabs(tmp):
    sys.path.append(str(tmp))  # add ROOT to PATH

from image.models import request_image
from pipe_cls import One2OnePipe, SplitMaincategory, IObserverPipe, ShallowCopyPipe
from DetectObjectPipe import DetectObjectPipe
from ClassficationPipe import ClassificationPipe
from pipe_utills import ImageCropPipe, SaveAttributesClassPipe
from Singleton import Singleton
from model_weights import (
    IWeight, OverallSubcategoryClassficationWeight, 
    OuterSubcategoryClassficationWeight, 
    BottomSubcategoryClassficationWeight, 
    TopSubcategoryClassficationWeight, PatternClassficationWeight
    #OverallPatternClassficationWeight, BottomPatternClassficationWeight, TopPatternClassficationWeight, OuterPatternClassficationWeight,
)
from detect_utills import (PipeResource, LoadImages,
                           copy_piperesource, is_test,
                           Annotator, cv2, print_args)

def is_test_factory()->bool:
    return True and is_test()

def test_print(s, s1="", s2="", s3="", s4="", s5="", end="\n"):
    if is_test_factory():
        print("factory pipe test : ", s, s1, s2, s3, s4, s5, end=end)

class Factory():
    def __init__(self, start_pipe=None, device='0', display = True):
        self.pipe = pipe_factory(start_pipe=start_pipe, device=device, display=display)
    
    
def pipe_factory(start_pipe=None, device='0', display = True):
    if display:
        print("initialize weights")
    # detect - spilte maincategory
    detect_cls_pipe = DetectObjectPipe(device=device, display=display)
    splite_main = SplitMaincategory()
    detect_cls_pipe.connect_pipe(splite_main) # connect
    
    # splite - ( attributes save )s
    for i, label in enumerate(splite_main.idx2label):
        if display:
            print(i, label, ": connect", end="")
        # img crop - repeat
        crop_pipe = ImageCropPipe()
        copy_pipe = ShallowCopyPipe()
        crop_pipe.connect_pipe(copy_pipe) # connect
        
        # # 패턴 카테고리 - 저장
        # classfication_pipe = ClassificationPipe(PatternClassficationWeight(display=display, device=device))
        # classfication_pipe.connect_pipe(SaveAttributesClassPipe(display=display)) # find - save
        # copy_pipe.connect_pipe(classfication_pipe) # repeater - (find&save)
        
        # find attribute - save attribute
        if label == "Overall":
            # 서브 카테고리 - 저장
            classfication_pipe = ClassificationPipe(OverallSubcategoryClassficationWeight(display=display, device=device))
            classfication_pipe.connect_pipe(SaveAttributesClassPipe(display=display)) # find - save
            copy_pipe.connect_pipe(classfication_pipe) # repeater - (find&save)
            
            # # 패턴 카테고리 - 저장
            # classfication_pipe = ClassificationPipe(OverallPatternClassficationWeight(display=display, device=device))
            # classfication_pipe.connect_pipe(SaveAttributesClassPipe(display=display)) # find - save
            # copy_pipe.connect_pipe(classfication_pipe) # repeater - (find&save)
            
            # # 컬러 카테고리 - 저장
            # classfication_pipe = ClassificationPipe(ClassficationWeight(display=display, device=device))
            # classfication_pipe.connect_pipe((display=display)) # find - save
            # copy_pipe.connect_pipe(classfication_pipe) # repeater - (find&save)
        elif label == "Bottom":
            # 서브 카테고리 - 저장
            classfication_pipe = ClassificationPipe(BottomSubcategoryClassficationWeight(display=display, device=device))
            classfication_pipe.connect_pipe(SaveAttributesClassPipe(display=display)) # find - save
            copy_pipe.connect_pipe(classfication_pipe) # repeater - (find&save)
            
            # # 패턴 카테고리 - 저장
            # classfication_pipe = ClassificationPipe(BottomPatternClassficationWeight(display=display, device=device))
            # classfication_pipe.connect_pipe(SaveAttributesClassPipe(display=display)) # find - save
            # copy_pipe.connect_pipe(classfication_pipe) # repeater - (find&save)
            
            # # 컬러 카테고리 - 저장
            # classfication_pipe = ClassificationPipe(ClassficationWeight(display=display, device=device))
            # classfication_pipe.connect_pipe((display=display)) # find - save
            # copy_pipe.connect_pipe(classfication_pipe) # repeater - (find&save)
        elif label == "Top":
            # 서브 카테고리 - 저장
            classfication_pipe = ClassificationPipe(TopSubcategoryClassficationWeight(display=display, device=device))
            classfication_pipe.connect_pipe(SaveAttributesClassPipe(display=display)) # find - save
            copy_pipe.connect_pipe(classfication_pipe) # repeater - (find&save)
            
            # # 패턴 카테고리 - 저장
            # classfication_pipe = ClassificationPipe(TopPatternClassficationWeight(display=display, device=device))
            # classfication_pipe.connect_pipe(SaveAttributesClassPipe(display=display)) # find - save
            # copy_pipe.connect_pipe(classfication_pipe) # repeater - (find&save)
            
            # # 컬러 카테고리 - 저장
            # classfication_pipe = ClassificationPipe(ClassficationWeight(display=display, device=device))
            # classfication_pipe.connect_pipe((display=display)) # find - save
            # copy_pipe.connect_pipe(classfication_pipe) # repeater - (find&save)
        elif label == "Outer":
            # 서브 카테고리 - 저장
            classfication_pipe = ClassificationPipe(OuterSubcategoryClassficationWeight(display=display, device=device))
            classfication_pipe.connect_pipe(SaveAttributesClassPipe(display=display)) # find - save
            copy_pipe.connect_pipe(classfication_pipe) # repeater - (find&save)
            
            # # 패턴 카테고리 - 저장
            # classfication_pipe = ClassificationPipe(OuterPatternClassficationWeight(display=display, device=device))
            # classfication_pipe.connect_pipe(SaveAttributesClassPipe(display=display)) # find - save
            # copy_pipe.connect_pipe(classfication_pipe) # repeater - (find&save)
            
            # # 컬러 카테고리 - 저장
            # classfication_pipe = ClassificationPipe(ClassficationWeight(display=display, device=device))
            # classfication_pipe.connect_pipe((display=display)) # find - save
            # copy_pipe.connect_pipe(classfication_pipe) # repeater - (find&save)
        _ = splite_main.connect_pipe(crop_pipe)
        if display:
            print(_)
    
    #set start_pipe end_pipe
    if start_pipe is None:
        start_pipe = detect_cls_pipe
    elif isinstance(start_pipe, IObserverPipe):
        start_pipe.connect_pipe(detect_cls_pipe)
    else:
        raise TypeError("TypeError in pipe_factory")
    return start_pipe

def test(src=FASHION_BASE_DIR / "media" / "test", 
         device='0', 
         display=True
         ):
    start_pipe = pipe_factory(device=device, display=display)
    
    ### Dataloader ###
    dataset = LoadImages(src)
    ### 실행 ###
    for im0, path, s in dataset:
        # 이미지 저장
        #   convert from BGR to RGB
        color_coverted = cv2.cvtColor(im0, cv2.COLOR_BGR2RGB)
        #   convert from openCV2 to PIL
        pil_image=Image.fromarray(color_coverted)
        img = request_image(requester_id=2, img=pil_image)
        
        # set piperesource
        metadata = {"path": path, "img_id":img.id}
        images = {"origin":im0}
        input = PipeResource(im=im0, metadata=metadata, images=images, s=s)
        # push input
        start_pipe.push_src(input)

    
def runner(args):
    print_args(vars(args))
    test(args.src, args.device, args.display)
    #run(args.src, args.device)
    # detect(args.src, args.device)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', default=FASHION_BASE_DIR / "media" / "test")
    parser.add_argument('--device', default='0', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--display', default=True, action="store_false")
    args = parser.parse_args()
    runner(args) 