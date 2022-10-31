from importlib.resources import Resource
import sys
from pathlib import Path
import torch
import argparse
import os
import time

FASHION_BASE_DIR=Path(__file__).resolve().parent.parent.parent
FILE = Path(__file__).resolve()
ROOT = FILE.parents
WEIGHT_DIR = None

# tmp = ROOT
# if str(tmp) not in sys.path and os.path.isabs(tmp):
#     sys.path.append(str(tmp))  # add ROOT to PATH
tmp = FASHION_BASE_DIR / 'weights'
if str(tmp) not in sys.path and os.path.isabs(tmp):
    WEIGHT_DIR= (str(tmp))  # add Weights ROOT to PATH

# tmp = ROOT + '/yolov5'
# if str(tmp) not in sys.path and os.path.isabs(tmp):
#     sys.path.append(str(tmp))  # add yolov5 ROOT to PATH
    
# ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative



from pipe_cls import *
from Singleton import Singleton

def is_test()->bool:
    return False

def test_print(s, s1="", s2="", s3="", s4="", s5="", end="\n"):
    if is_test():
        print("detect object pipe test : ", s, s1, s2, s3, s4, s5, end=end)
test_print(sys.path)

from yolov5.utils.plots import Annotator, colors, save_one_box
from yolov5.utils.torch_utils import select_device, time_sync
from yolov5.utils.general import (LOGGER, check_img_size, non_max_suppression, scale_coords, cv2, xyxy2xywh)
from yolov5.utils.dataloaders import VID_FORMATS, LoadImages, LoadStreams
from yolov5.models.common import DetectMultiBackend
############################

class DetectObjectWeight(metaclass=Singleton):
    def __init__(
        self,
        conf_thres=0.25,
        iou_thres=0.45,
        max_det=7,
        cls=[0, 1],
        imgsz=(640,640),
        device = '0'
        ) -> None:
        # 고정값
        WEIGHTS = WEIGHT_DIR + "/yolo_ball.pt"
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
        
        self.save_dir = 'save/'
        
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
            print(f'[YOLOv5 init {t2-t1}s]')

    @torch.no_grad()
    def exe(self, input: PipeResource) -> PipeResource:
        t1 = time.time()
        output = PipeResource()

        # 고정 값
        visualize = False
        agnostic_nms = False
        classes = None
        device = self.device
        model = self.model
        dt, seen = [0.0, 0.0, 0.0, 0.0], 0

        conf_thres = self.conf_thres
        iou_thres = self.iou_thres
        max_det = self.max_det

        t1 = time_sync()
        im = torch.from_numpy(input.im).to(device)
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

            p, im0, _ = input.path, input.im0s.copy(), getattr(input, 'frame', 0)
            p = Path(p)

            ## 추가 ##
            annotator = Annotator(
                im0, line_width=3, example=str(self.model.names))
            if len(det):
                det[:, :4] = scale_coords(
                    im.shape[2:], det[:, :4], im0.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)
                    label = None
                    annotator.box_label(xyxy, label, color=colors(c, True))

            #### 좌표 변환 ####
            cxywh = xyxy2xywh(det[:, 0:4])

            #### 바운딩 박스 & center x,y 점 ####
            im0 = annotator.result()
            for i in range(det.shape[0]):
                cv2.circle(im0, (int(cxywh[i][0]), int(
                    cxywh[i][1])), 4, (0, 255, 0), -1)

            ## output 설정 ###
            for i in range(det.shape[0]):
                output_det = {"frame": input.f_num, "x": int(det[i][0]), "y": int(det[i][1]), "w": int(
                    det[i][2]), "h": int(det[i][3]), "conf": float(det[i][4]), "cls": int(det[i][5])}
                input.dets.append(output_det)

        output = copy_piperesource(input)
        t2 = time.time()
        ball_det_len = output.len_detkey_match("cls", "1")
        ball_det_len = "" if ball_det_len == 3 else f"(det ball :{str(ball_det_len)})"
        if self.display:
            print(f'[{ball_det_len}YOLOv5 run {t2-t1:.3f}s]', end=" ")
        
        output.print(on=(is_test() and output.__len__() < 7))
        return output

    def get_regist_type(self, idx=0) -> str:
        return "det_obj"


    @torch.no_grad()
    def runascapp(self, input: PipeResource):
        t1 = time.time()
        output = []

        # 고정 값
        visualize = False
        agnostic_nms = False
        classes = None
        device = self.device
        model = self.model
        dt, seen = [0.0, 0.0, 0.0, 0.0], 0

        conf_thres = self.conf_thres
        iou_thres = self.iou_thres
        max_det = self.max_det

        t1 = time_sync()
        im = torch.from_numpy(input.im).to(device)
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

            p, im0, _ = input.path, input.im0s.copy(), getattr(input, 'frame', 0)
            p = Path(p)

            ## 추가 ##
            annotator = Annotator(
                im0, line_width=3, example=str(self.model.names))
            if len(det):
                det[:, :4] = scale_coords(
                    im.shape[2:], det[:, :4], im0.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)
                    label = None
                    annotator.box_label(xyxy, label, color=colors(c, True))

            #### 좌표 변환 ####
            cxywh = xyxy2xywh(det[:, 0:4])

            #### 바운딩 박스 & center x,y 점 ####
            im0 = annotator.result()
            for i in range(det.shape[0]):
                cv2.circle(im0, (int(cxywh[i][0]), int(
                    cxywh[i][1])), 4, (0, 255, 0), -1)

            ## output 설정 ###
            for i in range(det.shape[0]):
                output_det = {"frame": input.f_num, "x": int(det[i][0]), "y": int(det[i][1]), "w": int(
                    det[i][2]), "h": int(det[i][3]), "conf": float(det[i][4]), "cls": int(det[i][5])}
                input.dets.append(output_det)
                #print(f'{i}-{output_det}')
                output.append(output_det)
        
        t2 = time.time()
        
        if self.display:
            print(f'[{len(output)} YOLOv5 run {t2-t1:.3f}s]', end=" ")
        
        return output

    def get_regist_type(self, idx=0) -> str:
        return "det_obj"

def test(src, device):
    ### Pipe 생성 & 연결 ###
    detectObjectPipe1 = DetectObjectPipe(device=device)
    split_cls = SplitCls()
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
    test(args.src, args.device)
    #runascapp(args.src, args.device)
    #test_singleton()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', default= (FASHION_BASE_DIR / "media" / "test"))
    parser.add_argument('--device', default='0', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    args = parser.parse_args()
    runner(args) 

  