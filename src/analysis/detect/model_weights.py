from threading import Lock
from abc import *

from Singleton import Singleton
from detect_utills import (
    select_device, Path,
    LOGGER, is_test
)

############################
class IWeight(metaclass=ABCMeta):
    def __init__(
        self,
        conf_thres=0.25,
        imgsz=(640,640),
        cls=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        device = '0',
        ) -> None:
        self.device = select_device(device)
        
        # 변하는 값(입력 값)
        self.conf_thres = conf_thres
        # classes = None  # filter by class: --class 0, or --class 0 2 3
        self.cls = cls
        self.imgsz = imgsz  # inference size (height, width)
        self.lock = Lock()
    
    @abstractclassmethod
    def get_weights(self) -> Path:
        pass
    
class TopClassficationWeight(IWeight, metaclass=Singleton):
    def __init__(
        self, 
        conf_thres=0.25, 
        imgsz=(640, 640), 
        cls=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 
        device='0'
        ) -> None:
        
        super().__init__(conf_thres, imgsz, cls, device)
    