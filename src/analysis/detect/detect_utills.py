def is_test()->bool:
    return True

def test_print(s, s1="", s2="", s3="", s4="", s5="", end="\n"):
    if is_test():
        print("pipe cls exe : ", s, s1, s2, s3, s4, s5, end=end)

from random import random, randrange
import sys
import logging

from yolov5.utils.general import (xywh2xyxy, cv2)
from yolov5.utils.dataloaders import letterbox, np
from yolov5.utils.plots import Annotator, colors, save_one_box

class PipeResource:
    def __init__(self, im=None, metadata=dict(), images=dict(), s=None) -> None:
        self.im = im            # target image
        self.dets = list()
        self.unset_det_num = dict()
        
        # get dateset  (path, im, im0s, vid_cap, s)
        self.metadata=dict()
        self.metadata.update(metadata)
        # images
        self.images=dict()
        self.images.update(images)
    
    def __iter__(self):
        self.count = 0
        return self
    
    def __next__(self) -> dict:
        if self.count == self.__len__():
            raise StopIteration
        
        cnt = self.count 
        
        contents = self.dets[cnt]
        
        self.count += 1
        
        return contents
    
    def __len__(self):
        #test_print("len ==>",self.dets.__len__())
        return self.dets.__len__()
    
    def print(self, on=True):
        if on:
            print("==============================================")
            print(f'{self.metadata["s"]}',"dets")
            for i, det in enumerate(self.dets):
                print(f'det {i} :', det)
            print("==============================================")
        
    def auto_set_dets(self):
        for i in range(randrange(1, 7)):
            det = {"xmin": randrange(10,1970), "ymin": randrange(10,1070), "xmax":randrange(18,31), "ymax":randrange(18,31), "Maincategory":randrange(0,2), "conf":random()}
            self.dets.append(det)
    def set_det(self, idx=0, xyxy=None, maincategory=0, conf=0.0):
        #test_print(self.dets.__len__(), "det.len()")
        if self.dets.__len__() < idx:
            raise IndexError
        if xyxy is not None:
            det = self.dets[idx]
            det["xmin"] = xyxy[0]
            det["ymin"] = xyxy[1]
            det["xmax"] = xyxy[2]
            det["ymax"] = xyxy[3]
            det["Maincategory"] = maincategory
            det["conf"] = conf

    def append_det(self, xywh, id=-1, maincategory=0, conf=0.0):
        det = dict()
        det["xmin"] = xywh[0]
        det["ymin"] = xywh[1]
        det["xmax"] = xywh[2]
        det["ymax"] = xywh[3]
        det["id"] = id
        det["Maincategory"] = maincategory
        det["conf"] = conf
        self.dets.append(det)
            
    def imshow(self, name="no name", idx_names=["1","2","3","4","5","6"],cls_names=["Overall", "Bottom", "Top", "Outer","Shose"],line_thickness=2, hide_labels=True, hide_conf = True):
        im0= self.images["origin"]
        annotator = Annotator(
            im0, line_width=line_thickness, example=str(cls_names))
        # Write results
        for i, det in enumerate(self.dets):
            c = int(det["Maincategory"])  # integer class
            id = ""
            try:
               id = f"{idx_names[int(det['id'])]} "
            except KeyboardInterrupt:sys.exit()
            except:
                pass
            label = None if hide_labels else (f"{id}{cls_names[c]}" if hide_conf else f'{cls_names[c]} {det["conf"]:.2f}')
            xywh = [det["xmin"], det["ymin"], det["xmax"], det["ymax"]]
            xyxy = xywh2xyxy(xywh)
            annotator.box_label(xyxy, label, color=colors(c, True))
        im0 = annotator.result()
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(name, 1280, 720)
        cv2.imshow(name, im0)
        
    def is_detkey(self, key = "id") ->bool:
        try:
            for det in self.dets:
                a = det[key]
                test_print(f"is_detkey({key} : {a})")
        except KeyboardInterrupt:sys.exit()
        except:
            return False
        return True
    
    def len_unset_detkey(self, key = "id") -> int:
        try:
            return self.unset_det_num[key]
        except KeyboardInterrupt:sys.exit()
        except:
            cnt = 0
            for det in self.dets:
                try:
                    a = det[key]
                    test_print(f"is_detkey({key} : {a})")
                except:
                    cnt += 1
            self.unset_det_num[key] = cnt
            return self.unset_det_num[key]
    def len_detkey_match(self, key = "Maincategory", value="1") -> int:
        cnt = 0
        if len(self.dets) <= 0:
            return 0
        
        for det in self.dets:
            if int(det[key]) == int(value):
                cnt += 1
        return cnt
    def update_id(self, key, value, xywh, conf, cls=1):
        for det in self.dets:
            if float(det["conf"]) == float(conf) and int(det["Maincategory"]) == int(cls):
                if same_box([],[]):
                    det[key] = value
                        
def same_box(box1, box2, iou_th=0.9) -> bool:
    return True

def xywh2xyxy(x):
    y=list(x)
    y[0] = float(x[0]) - float(x[2]) / 2  # top left x
    y[1] = float(x[1]) - float(x[3]) / 2  # top left y
    y[2] = float(x[0]) + float(x[2]) / 2  # bottom right x
    y[3] = float(x[1]) + float(x[3]) / 2  # bottom right y
    return y

def xyxy2xywh(x):
    y=list(x)
    y[0] = (float(x[0]) + float(x[2])) / 2  # x center
    y[1] = (float(x[1]) + float(x[3])) / 2  # y center
    y[2] = float(x[2]) - float(x[0])  # width
    y[3] = float(x[3]) - float(x[1]) # height
    return y

def copy_piperesource(src:PipeResource)->PipeResource:
    dst = PipeResource()
    
    
    dst.dets = src.dets.copy()
    dst.im = src.im.copy()      # image
    
    # get dateset  (path, im0s, vid_cap, s)
    dst.metadata.update(src.metadata)
    for key, value in src.images.items:
        dst.images[key] = value.copy()
        
    return dst

def make_padding_image(im0, img_size=640, stride=32, auto=True, transforms=None):
    if transforms:
        dst = transforms(im0)
    else:
        dst = letterbox(im0, img_size, stride=stride, auto=auto)[0]  # padded resize
        dst = dst.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        dst = np.ascontiguousarray(dst)  # contiguous
    return dst

import os
import platform
def is_colab():
    # Is environment a Google Colab instance?
    return 'COLAB_GPU' in os.environ
def is_kaggle():
    # Is environment a Kaggle Notebook?
    return os.environ.get('PWD') == '/kaggle/working' and os.environ.get('KAGGLE_URL_BASE') == 'https://www.kaggle.com'

RANK = int(os.getenv('RANK', -1)) # rank in world for Multi-GPU trainings
VERBOSE = str(os.getenv('Fashion_VERBOSE', True)).lower() == 'true'  # global verbose mode
def emojis(str=''):
    # Return platform-dependent emoji-safe version of string
    return str.encode().decode('ascii', 'ignore') if platform.system() == 'Windows' else str
def set_logging(name=None, verbose=VERBOSE):
    # Sets level and returns logger
    if is_kaggle() or is_colab():
        for h in logging.root.handlers:
            logging.root.removeHandler(h)  # remove all handlers associated with the root logger object
    rank = RANK
    level = logging.INFO if verbose and rank in {-1, 0} else logging.ERROR
    log = logging.getLogger(name)
    log.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    handler.setLevel(level)
    log.addHandler(handler)
    
set_logging()  # run before defining LOGGER
LOGGER = logging.getLogger("fashion_detector")  # define globally (used in train.py, val.py, detect.py, etc.)
if platform.system() == 'Windows':
    for fn in LOGGER.info, LOGGER.warning:
        setattr(LOGGER, fn.__name__, lambda x: fn(emojis(x)))  # emoji safe logging