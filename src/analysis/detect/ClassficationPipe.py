import torch
import argparse
import time

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
from detect_utills import (PipeResource, LoadImages,
                           make_padding_image, copy_piperesource,
                           LOGGER, is_test,
                           Annotator, colors, save_one_box, cv2)
def is_test_classfication()->bool:
    return True and is_test()

def test_print(s, s1="", s2="", s3="", s4="", s5="", end="\n"):
    if is_test_classfication():
        print("detect object pipe test : ", s, s1, s2, s3, s4, s5, end=end)

############################
from threading import Lock
from abc import *

def test(src, device, display=True):
    ### Pipe 생성###
    detectObjectPipe1 = DetectObjectPipe(device=device, display=display)
    bag_split = ResourceBag()
    
    # 파이프 연결
    detectObjectPipe1.connect_pipe(bag_split)
    ### Dataloader ###
    dataset = LoadImages(src)
    ### 실행 ###
    for im0, path, s in dataset:
        metadata = {"path": path}
        images = {"origin":im0}
        input = PipeResource(im=im0, metadata=metadata, images=images, s=s)
        detectObjectPipe1.push_src(input)
    
    # bag_split.print()
    if display:
        for src in bag_split.src_list:
            src.imshow(name="hellow")
            cv2.waitKey(1000)

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