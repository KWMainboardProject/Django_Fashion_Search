import argparse
import os
from pathlib import Path
import sys

FILE = Path(__file__).resolve()
ROOT = FILE.parents


from yolov5.utils.dataloaders import VID_FORMATS, LoadImages, LoadStreams
from DetectObjectPipe import DetectObjectPipe
from pipe_cls import IObserverPipe, ConvertToxywhPipe, PipeResource, ResourceBag, SplitCls, SplitIdx, FirstCopyPipe, StartNotDetectCutterPipe, xyxy2xywh, test_print

def pipe_factory(start_pipe=None, device='cpu', display = True):
    if display:
        print("initialize weights")
    #detect class and split class
    detect_cls_pipe = DetectObjectPipe(device=device, display=display)
    split_cls_pipe = SplitCls()
    
    



def detect(src, device='cpu', MIN_DETS= 10, display=True):
     ### Dataloader ###
    source = src
    imgsz = (640, 640)
    pt = True
    stride = 32
    nr_sources = 1

    dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)
    vid_path, vid_writer, txt_path = [
        None] * nr_sources, [None] * nr_sources, [None] * nr_sources

    # set pipe
    pipe, ball_bags, edge_bag = pipe_factory(device=device, display=display)
    
    ### 실행 ###
    for frame_idx, (path, im, im0s, vid_cap, s) in enumerate(dataset):
        input = PipeResource(f_num=frame_idx, path=path,
                             im=im, im0s=im0s, vid_cap=vid_cap, s=s)
        pipe.push_src(input)
    
    ball_bag_list = []
    
    # cut index
    for i, bag in enumerate(reversed(ball_bags)):
        cnt = 0
        for resource in bag.src_list:
            # counting det num
            if resource.__len__() > 0 :
                resource.print()
                cnt += 1
                test_print(f"cnt({cnt})")
        if cnt > MIN_DETS : 
            test_print(f"{i} bag cnt({cnt})")
            ball_bag_list.append(bag)
    
    return (ball_bag_list, edge_bag)
    
def test(src, device):
    ball_bag_list, edge_bag = detect(src, device)
     
    title = "test"
    for ball_bag in ball_bag_list:
        for ball_det in ball_bag.src_list:
            ball_det.imshow(title, idx_names=["1","2","3","4","5","6"], hide_labels=False)
    print("edge : ", edge_bag.get_edge())
    
def runner(args):
    test(args.src, args.device)
    #run(args.src, args.device)
    detect(args.src, args.device)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', default="/../../data/videos/kj_cud_272.mp4")
    parser.add_argument('--device', default='0', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    args = parser.parse_args()
    print(args.src)
    runner(args) 