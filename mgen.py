import os 
import argparse
import time 

from utils.mgenutil.setting import getDatasets
from utils.general import changeAbsPath,check_dir_list,path_confirm,str2bool
from utils.mgenutil.func import drawSeg

def parser_opt(known=False):
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-lp","--LabelPath",dest="LabelPath",type=str,default="./labels",help= "Files(json or txt) directory path")
    parser.add_argument("-ip",'--ImagePath',dest = "ImagePath",type=str,default="./images",help = "Filse (image) directory path")
   
    parser.add_argument("-refer","--colorCoordinate",dest ="ColorCoordinate",type=str,default="./refer/img_coor.json",help ="Dictionary : Unreal color coordinate")
    # parser.add_argument("-b","--background",dest="backGround",type = str2bool,default=True)
    # parser.add_argument("-lw","--LineWidth",dest="LineWidth",type=float,default=0.3)
    parser.add_argument("-cls_set","--ClassYaml",dest="ClassYaml",type=str,default="./refer/cls.yaml")
    parser.add_argument("-colo_set","--colorSetting",dest ="colorSetting",type=str,default="./refer/color.yaml")
    parser.add_argument("-sr","--saveRoot",dest='SavePath',type=str,default="./result/")
    
    # mgen 추가적인 option 
    parser.add_argument("-seg",'--SegImgPath',dest = "SegImPath",type=str,default="./seg",help = "Filse (seg image) directory path")
    
    args = parser.parse_args()
    return parser.parse_known_args()[0] if known else parser.parse_args()

def main(opt):
    _label = changeAbsPath(opt.LabelPath,"-lp")
    _image = changeAbsPath(opt.ImagePath,"-ip")
    _labels = check_dir_list(_label,"-lp")
    _refer_Coord = changeAbsPath(opt.ColorCoordinate,"-refer")
    _refer_cls = changeAbsPath(opt.ClassYaml,"-cls_set")
    _refer_color = changeAbsPath(opt.colorSetting,"-colo_set")
    _seg = changeAbsPath(opt.SegImPath,"-seg")
    _savepath = path_confirm(opt.SavePath)
    _sr = changeAbsPath(_savepath,"-sr")

    # path 
    yoloSave = path_confirm(os.path.join(_sr,"YoloForm/"))
    newSegImgSave = path_confirm(os.path.join(_sr,"MgenFormSegImg/"))
    confirmImgSave =  path_confirm(os.path.join(_sr,"ConfrimImg/"))

    dataset = getDatasets(
        _labels,
        _image,
        _seg,
        _refer_cls,
        _refer_color
    )

    drawSeg(dataset.getDataset(),_refer_Coord,newSegImgSave,yoloSave)


if __name__ == "__main__":
    start = time.time()
    opt = parser_opt(True)
    main(opt)
    end = time.time()
    print(f"{end-start:.5f} sec")