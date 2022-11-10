from threading import Lock
from abc import *
import time
import torch


# set path
import sys
from pathlib import Path
import os


FILE = Path(__file__).resolve()
ROOT = FILE.parent
# tmp = ROOT / "yolov5"
# if str(tmp) not in sys.path and os.path.isabs(tmp):
#     sys.path.append(str(tmp))  # add ROOT to PATH

WEIGHT_DIR = None
FASHION_BASE_DIR=Path(__file__).resolve().parent.parent.parent
tmp = FASHION_BASE_DIR / 'weights'
if str(tmp) not in sys.path and os.path.isabs(tmp):
    WEIGHT_DIR= (tmp)  # add Weights ROOT to PATH

from Singleton import Singleton
from detect_utills import (
    select_device, Path,
    LOGGER, is_test
)

def is_test_Weight()->bool:
    return True and is_test()

def test_print(s, s1="", s2="", s3="", s4="", s5="", end="\n"):
    if is_test_Weight():
        print("weight pipe test : ", s, s1, s2, s3, s4, s5, end=end)

############################
class IWeight:
    cls=None # list!!!
    WEIGHTS=None # Path
    NAME=None
    ATTRBUTES_TYPE_ID=None
    def __init__(
        self,
        display=True,
        conf_thres=0.25,
        imgsz=(224, 224),
        device = '0',
        cls=None,
        weights_path=None,
        name=None,
        id=None
        ) -> None:
        if cls is not None: self.cls=cls
        if weights_path is not None: self.WEIGHTS=weights_path
        if name is not None: self.NAME=name
        if id is not None: self.ATTRBUTES_TYPE_ID=id
        t1 = time.time()
        # Select device
        self.device = select_device(model_name=self.NAME,device=device)
        # 변하는 값(입력 값)
        self.conf_thres = conf_thres
        self.imgsz = imgsz  # inference size (height, width)
        self.lock = Lock()
        self.display = display

        # weight2gpu
        model = torch.load(self.WEIGHTS)
        # if is_test_Weight():
        #     print(model)
        try:             model.eval()
        except: pass
        model = model.to(self.device)
        self.model = model
        t2 = time.time()
        print( f'[{self.NAME} init {(t2-t1):.1f}s]')
class OverallSubcategoryClassficationWeight(IWeight, metaclass=Singleton):
    cls=["Jumpsuit", "Onepiece Dress"]
    WEIGHTS=WEIGHT_DIR / "Overall_classification.pt"
    NAME="Resnet34 Overall Subcategory Classicication"
    ATTRBUTES_TYPE_ID = 1
    def __init__(self, display=True, conf_thres=0.25, imgsz=(224, 224), device='0', cls=None, weights_path=None, name=None, id=None) -> None:
        super().__init__(display, conf_thres, imgsz, device, cls, weights_path, name, id)
class BottomSubcategoryClassficationWeight(IWeight, metaclass=Singleton):
    cls=["Jogger Pants","Long Pants","Long Skirt","Mini Skirt","Short Pants"]
    WEIGHTS=WEIGHT_DIR / "Bottom_classification.pt"
    NAME="Resnet34 Bottom Subcategory Classicication"
    ATTRBUTES_TYPE_ID = 5
    def __init__(self, display=True, conf_thres=0.25, imgsz=(224, 224), device='0', cls=None, weights_path=None, name=None, id=None) -> None:
        super().__init__(display, conf_thres, imgsz, device, cls, weights_path, name, id)  
class TopSubcategoryClassficationWeight(IWeight, metaclass=Singleton):
    cls=['Hoodie', 
         'Long sleeve shirts', 
         'Long sleeve tee', 
         'Pullover', 
         'Short sleeve shirts', 
         'Short sleeve tee', 
         'Sleeveless', 
         'Turtleneck']
    WEIGHTS=WEIGHT_DIR / "Top_classification.pt"
    NAME="Resnet34 Top Subcategory Classicication"
    ATTRBUTES_TYPE_ID = 9
    def __init__(self, display=True, conf_thres=0.25, imgsz=(224, 224), device='0', cls=None, weights_path=None, name=None, id=None) -> None:
        super().__init__(display, conf_thres, imgsz, device, cls, weights_path, name, id)
class OuterSubcategoryClassficationWeight(IWeight, metaclass=Singleton):
    cls=["Blazer Jacket",
            "Long Hoodie",
            "Long NoHood",
            "Short Blouson",
            "Short Hoodie",
            "Short None",
            "Short Normal",
            "Short Stand",
            "Vest"        ]
    WEIGHTS=WEIGHT_DIR / "Outer_classification.pt"
    NAME="Resnet34 Outer Subcategory Classicication"
    ATTRBUTES_TYPE_ID = 13
    def __init__(self, display=True, conf_thres=0.25, imgsz=(224, 224), device='0', cls=None, weights_path=None, name=None, id=None) -> None:
        super().__init__(display, conf_thres, imgsz, device, cls, weights_path, name, id)
        
class PatternClassficationWeight(IWeight, metaclass=Singleton):
    cls=[
            "animal", 
            "argyle", 
            "camouflage", 
            "check", 
            "dot", 
            "lettering",
            "printing", 
            "solid",
            "stripe",
            "tropical"
        ]
    WEIGHTS=WEIGHT_DIR / "pattern.pt"
    NAME="Resnet34 Pattern Classicication"
    ATTRBUTES_TYPE_ID = 2
    def __init__(self, display=True, conf_thres=0.25, imgsz=(224, 224), device='0', cls=None, weights_path=None, name=None, id=None) -> None:
        super().__init__(display, conf_thres, imgsz, device, cls, weights_path, name, id)
"""       
class OverallPatternClassficationWeight(IWeight, metaclass=Singleton):
    cls=[
            "animal", 
            "argyle", 
            "camouflage", 
            "check", 
            "dot", 
            "lettering",
            "printing", 
            "solid",
            "stripe",
            "tropical"
        ]
    WEIGHTS=WEIGHT_DIR / "pattern.pt"
    NAME="Resnet34 Overall Pattern Classicication"
    ATTRBUTES_TYPE_ID = 2
    def __init__(self, display=True, conf_thres=0.25, imgsz=(224, 224), device='0', cls=None, weights_path=None, name=None, id=None) -> None:
        super().__init__(display, conf_thres, imgsz, device, cls, weights_path, name, id)
class BottomPatternClassficationWeight(IWeight, metaclass=Singleton):
    cls=[
            "solid",
        ]
    WEIGHTS=WEIGHT_DIR / "pattern.pt"
    NAME="Resnet34 Bottom Pattern Classicication"
    ATTRBUTES_TYPE_ID = 6
    def __init__(self, display=True, conf_thres=0.25, imgsz=(224, 224), device='0', cls=None, weights_path=None, name=None, id=None) -> None:
        super().__init__(display, conf_thres, imgsz, device, cls, weights_path, name, id)     
class TopPatternClassficationWeight(IWeight, metaclass=Singleton):
    cls=[
            "animal", 
            "argyle", 
            "camouflage", 
            "check", 
            "dot", 
            "lettering",
            "printing", 
            "solid",
            "stripe",
            "tropical"
        ]
    WEIGHTS=WEIGHT_DIR / "pattern.pt"
    NAME="Resnet34 Top Pattern Classicication"
    ATTRBUTES_TYPE_ID = 10
    def __init__(self, display=True, conf_thres=0.25, imgsz=(224, 224), device='0', cls=None, weights_path=None, name=None, id=None) -> None:
        super().__init__(display, conf_thres, imgsz, device, cls, weights_path, name, id) 
class OuterPatternClassficationWeight(IWeight, metaclass=Singleton):
    cls=[
            "animal", 
            "argyle", 
            "camouflage", 
            "check", 
            "dot", 
            "lettering",
            "printing", 
            "solid",
            "stripe",
            "tropical"
        ]
    WEIGHTS=WEIGHT_DIR / "pattern.pt"
    NAME="Resnet34 Outer Pattern Classicication"
    ATTRBUTES_TYPE_ID = 14
    def __init__(self, display=True, conf_thres=0.25, imgsz=(224, 224), device='0', cls=None, weights_path=None, name=None, id=None) -> None:
        super().__init__(display, conf_thres, imgsz, device, cls, weights_path, name, id)
        
"""