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
    _refer_color = changeAbsPath(opt.colorSetting,"opt.cs")

    datsets = getDatasets(_labels,
                          _image,
                          _refer_cls,
                          _refer_Coord,
                          _refer_color,
                          opt.CompanyTask)
    # 세그멘테이션 그리기 
    ConfirmImage(datsets.getDataset(),
                 opt.backGround,
                 opt.LineWidth,
                 )
    
    


def parser_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument("-task","--LabelType",dest = "LabelType",type=str,default="seg",help="[\'seg\',\'bbox\']")
    parser.add_argument("-lp","--LabelPath",dest="LabelPath",type=str,default="./labels",help= "Files(json or txt) directory path")
    parser.add_argument("-ip",'--ImagePath',dest = "ImagePath",type=str,default="./images",help = "Filse (image) directory path")
    parser.add_argument("-refer","--colorCoordinate",dest ="ColorCoordinate",type=str,default="./refer/img_coor.json",help ="Dictionary : Unreal color coordinate")

    parser.add_argument("-b","--background",dest="backGround",type = str2bool,default=True)
    parser.add_argument("-lw","--LineWidth",dest="LineWidth",type=float,default=0.3)
    parser.add_argument("-cls_set","--ClassYaml",dest="ClassYaml",type=str,default="./refer/cls.yaml")
    parser.add_argument("-colo_set","--colorSetting",dest ="colorSetting",type=str,default="./refer/color.yaml")
    parser.add_argument("-sr","--saveRoot",dest="saveRoot",type=str,default="./result")
     
    
    args = parser.parse_args()
    return parser.parse_known_args()[0] if known else parser.parse_args()
 
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

