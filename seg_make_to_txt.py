import os 
import shutil
import json
import time
import argparse
from utils.general import *
from utils.func import *
from utils.setting import *

try:
    from easydict import EasyDict as edict
except:
    os.system("pip install pillow")
    os.system("pip install easydict")
    os.system("pip install opencv-python")
    
COLOR_COORDINATE = "./refer/img_coor.json"
IMAGE = "./images"
TXT_PATH = "./labels"


def parser_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument("-b","--background",dest="backGround",default=True)
    args = parser.parse_args()
    return parser.parse_known_args()[0] if known else parser.parse_args()

def UnrealTransefomrYolo():
    SEG_PATH = "./seg"
    JSON_PATH = "./json/"
    seg = check_dir_list(SEG_PATH,"main.py SEG_PATH")
    js = check_dir_list(JSON_PATH,"main.py JSON_PATH")

    yolo_label_dir = path_confirm("./yolo/")
    new_seg_folder = path_confirm("./fire_smoke_new_seg_im/")
    confirm_img_seg = path_confirm("./convert_confirm")
    cstart = time.time()
    [shutil.copy2(i,os.path.join(new_seg_folder,i)) for i in seg] # copy segmentation Image 
    cend=time.time()
    print(f"Copy Complet {cend-cstart:.5f} sec")

def readJsonDraw():
    """
    Unreal DataSet Transeform yolo format Dataset 

    """
    pass 

def readTxtDraw():    
    imagePath = IMAGE
    txt = check_dir_list(TXT_PATH,"TXT_PATH")
    for t in txt:
       
        obj=getDataInfo(t,
                    IMAGE
                    )
        ConfirmImage(obj)

def UnrealColorCoord(ColorCoordinate):
    def json_dict(jpth):
        with open(jpth,"r",encoding='cp949') as f:
            js = edict(json.load(f))
        return js
    img_coor_json = json_dict(ColorCoordinate)
    return img_coor_json

if __name__ =="__main__":
    start = time.time()
    s = readTxtDraw()
    end = time.time()
    print(f"{end-start:.5f} sec")

