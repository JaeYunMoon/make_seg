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
    

def run(opt):
    
    _label = changeAbsPath(opt.LabelPath,"opt.lp")
    _image = changeAbsPath(opt.ImagePath,"opt.ip")
    _labels = check_dir_list(_label,"opt.lp")
    _refer_Coord = changeAbsPath(opt.ColorCoordinate,"opt.refer")
    _refer_cls = changeAbsPath(opt.ClassYaml,"opt.cls_yaml")

    datsets = getDatasets(_labels,
                          _image,
                          _refer_cls,
                          _refer_Coord,
                          opt.CompanyTask)
    # 세그멘테이션 그리기 
    ConfirmImage(datsets,
                 opt.backGround,
                 opt.LineWidth,
                 )
    


def parser_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument("-lt","--LabelType",dest = "LabelType",type=str,default="txt",help="[\'txt\',\'json\']")
    parser.add_argument("-lp","--LabelPath",dest="LabelPath",type=str,default="./labels",help= "Files(json or txt) directory path")
    parser.add_argument("-ip",'--ImagePath',dest = "ImagePath",type=str,default="./images",help = "Filse (image) directory path")
    parser.add_argument("-refer","--colorCoordinate",dest ="ColorCoordinate",type=str,default="./refer/img_coor.json",help ="Dictionary : Unreal color coordinate")

    parser.add_argument("-b","--background",dest="backGround",type = str2bool,default=True)
    parser.add_argument("-lw","--LineWidth",dest="LineWidth",type=float,default=0.3)
    parser.add_argument("-cls_yaml","--ClassYaml",dest="ClassYaml",type=str,default="./refer/cls.yaml")
    parser.add_argument("-ct","--CompanyTask",dest="CompanyTask",type = str2bool,default=False,
                        help="엠젠 전용으로 시작하지만 유지보수를 위한 옵션, 이 옵션은 label이 json 자료형이여야 한다. 구현 아직안함")   
     
    
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
    opt = parser_opt(True)
    run(opt)
    end = time.time()
    print(f"{end-start:.5f} sec")

