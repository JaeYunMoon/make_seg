import os 
import argparse
from easydict import EasyDict as edict 
from utils.mgenutil.finish import compare_and_record,moveFile
from utils.general import str2bool,changeAbsPath,check_dir_list,path_confirm


def parse_opt(known="False"):
    parser=argparse.ArgumentParser()
    parser.add_argument("--chroma",dest="Chroma",type = str2bool,default=False,help = "Whether chroma is enabled or not")
    parser.add_argument("-cimg","--ConfirmImage",dest="ConfrimImage",default="./result/ConfrimImg")
    parser.add_argument("-seg","--SegImage",dest="SegImage",type = str,default="./datasets/seg")
    parser.add_argument("-oimg","--OriginImage",dest="OriginImage",type=str,default="./datasets/train/images")
    parser.add_argument("-l","--label",dest="Label",default="./datasets/json",type=str)
    parser.add_argument("-fm","--fileMove",dest="fileMove",type=str2bool,default=False)
    parser.add_argument("-sr","--SaveRoot",dest="SaveRoot",type=str,default="./result/")
    args = parser.parse_args()
    return parser.parse_known_args()[0] if known else parser.parse_args()

def main(opt):
    _label = changeAbsPath(opt.LabelPath,"-lp")
    _labels = check_dir_list(_label,"-lp")
    _confirmIm = changeAbsPath(opt.ConfrimImage,"-cimg")
    _confirmIms = check_dir_list(_confirmIm,"-cimg")
    
    _image = changeAbsPath(opt.OriginImage,"-oimg")
    _images = check_dir_list(_image,"-oimg")

    _seg = changeAbsPath(opt.SegImPath,"-seg")
    _segs = check_dir_list(_seg,"-seg")
    
    _savepath = path_confirm(opt.SavePath)
    _sr = changeAbsPath(_savepath,"-sr")
    removetxt = os.path.join(_sr,"Remove.txt") 
    removeTxt = compare_and_record(_image,_confirmIm,removetxt)

    _label_remove = moveFile(_label,removeTxt,opt.SaveRoot,"label")
    _image_remove = moveFile(_image,removeTxt,opt.SaveRoot,"images")
    _seg_remove = moveFile(_seg,removeTxt,opt.SaveRoot,"chroma")
    
    



    # 크로마 이미지 저장소 
    # copy 이미지 저장소 
    # txt파일로 항목 확인 후 지울지 copy할지 




if __name__=="__main__":
    opt = parse_opt()
    main(opt)