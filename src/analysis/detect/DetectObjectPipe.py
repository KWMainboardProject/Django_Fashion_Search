import torch
import argparse
import time

from yolov5.utils.torch_utils import select_device, time_sync
from yolov5.utils.general import (check_img_size, non_max_suppression, scale_coords, cv2, xyxy2xywh)
from yolov5.utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from yolov5.models.common import DetectMultiBackend


# set path
import sys
from pathlib import Path
import os

FILE = Path(__file__).resolve()
ROOT = FILE.parents
WEIGHT_DIR = None

FASHION_BASE_DIR=Path(__file__).resolve().parent.parent.parent
tmp = FASHION_BASE_DIR / 'weights'
if str(tmp) not in sys.path and os.path.isabs(tmp):
    WEIGHT_DIR= (str(tmp))  # add Weights ROOT to PATH

# import my project
from Singleton import Singleton
from pipe_cls import One2OnePipe, SplitMaincategory, ResourceBag
from detect_utills import PipeResource, make_padding_image, copy_piperesource, Annotator, colors, save_one_box, LOGGER, is_test

def is_test_detect_object()->bool:
    return False and is_test()

def test_print(s, s1="", s2="", s3="", s4="", s5="", end="\n"):
    if is_test_detect_object():
        print("detect object pipe test : ", s, s1, s2, s3, s4, s5, end=end)
test_print(sys.path)


############################



class DetectObjectWeight(metaclass=Singleton):
    def __init__(
        self,
        conf_thres=0.25,
        iou_thres=0.45,
        max_det=7,
        cls=[0, 1, 2, 3],
        imgsz=(640,640),
        device = '0'
        ) -> None:
        # 고정값
        WEIGHTS = WEIGHT_DIR / "FashionDetector.pt"
        self.yolo_weights = WEIGHTS
        self.device = select_device(device)
        
        # 변하는 값(입력 값)
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.max_det = max_det
        # classes = None  # filter by class: --class 0, or --class 0 2 3
        self.cls = cls
        self.imgsz = imgsz  # inference size (height, width)
        
        ### load model ###
        self.model = DetectMultiBackend(
            self.yolo_weights, device=self.device, dnn=False, data=None, fp16=False)
        ############
        
        self.imgsz = check_img_size(
            self.imgsz, s=self.model.stride)  # check image size
        
        self.model.warmup(imgsz=(1, 3, *self.imgsz))  # warmup

class DetectObjectPipe(One2OnePipe):  
    def __init__(self, device, display=True):
        super().__init__()
        self.display = display
        t1 = time.time()
        
        #load model
        instance = DetectObjectWeight(device=device)
        self.model = instance.model
        self.device = instance.device
        self.conf_thres = instance.conf_thres
        self.iou_thres = instance.iou_thres
        self.max_det = instance.max_det
        self.imgsz = instance.imgsz
        
        t2 = time.time()
        if display:
            LOGGER.info( f'[YOLOv5 init {(t2-t1):.1f}s]')
    
        
    @torch.no_grad()
    def exe(self,
            input: PipeResource,
            visualize = False,
            agnostic_nms = False,
            classes = None
            ) -> PipeResource:
        t1 = time.time()
        output = PipeResource()

        # 고정 값
        device = self.device
        model = self.model
        dt, seen = [0.0, 0.0, 0.0, 0.0], 0

        conf_thres = self.conf_thres
        iou_thres = self.iou_thres
        max_det = self.max_det

        t1 = time_sync()
        
        im = make_padding_image(input.im) # add padding
        im = torch.from_numpy(im).to(device)
        im = im.float()  # im.half() if half else im.float()  # uint8 to fp16/32
        im /= 255.0  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        t2 = time_sync()
        dt[0] += t2 - t1

        # Inference
        pred = model(im, augment=False, visualize=visualize)
        t3 = time_sync()
        dt[1] += t3 - t2

        # Apply NMS
        pred = non_max_suppression(
            pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        dt[2] += time_sync() - t3

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            seen += 1

            ## output 설정 ###
            for i in range(det.shape[0]):
                output_det = {"xmin": int(det[i][0]), "ymin": int(det[i][1]), "xmax": int(
                    det[i][2]), "ymax": int(det[i][3]), "conf": float(det[i][4]), "cls": int(det[i][5])}
                input.dets.append(output_det)

        output = copy_piperesource(input)
        t2 = time.time()
        detect_len = output.len_detkey_match("cls", "1")
        detect_len = "" if detect_len == 3 else f"(det ball :{str(detect_len)})"
        if self.display:
            LOGGER.info(f'[{detect_len}YOLOv5 run {t2-t1:.3f}s]')
        
        output.print(on=(is_test_detect_object() and output.__len__() < 7))
        return output

    def get_regist_type(self, idx=0) -> str:
        return "det_maincategory"

def test(src, device):
    ### Pipe 생성 & 연결 ###
    detectObjectPipe1 = DetectObjectPipe(device=device)
    split_cls = SplitMaincategory()
    detectObjectPipe1.connect_pipe(split_cls)

    ### SplitCls 생성 & 연결 ###
    bag_split = ResourceBag()
    
    ### Dataloader ###
    source = src
    imgsz = (640, 640)
    pt = True
    stride = 32
    nr_sources = 1

    dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)
    vid_path, vid_writer, txt_path = [
        None] * nr_sources, [None] * nr_sources, [None] * nr_sources

    ### 실행 ###
    for frame_idx, (path, im, im0s, vid_cap, s) in enumerate(dataset):
        input = PipeResource(f_num=frame_idx, path=path,
                             im=im, im0s=im0s, vid_cap=vid_cap, s=s)
        detectObjectPipe1.push_src(input)
    
    bag_split.print()

def test_singleton():
    gpu = DetectObjectPipe(device="cpu")
    #cpu = DetectObjectPipe(device="0")
    
    print(id(gpu.model))
    #print(id(cpu.model))

def runner(args):
    pass
    # test(args.src, args.device)
    #runascapp(args.src, args.device)
    #test_singleton()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', default= (FASHION_BASE_DIR / "media" / "test"))
    parser.add_argument('--device', default='0', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    args = parser.parse_args()
    runner(args) 

  
