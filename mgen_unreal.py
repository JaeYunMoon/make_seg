# Mgen 데이터 출력 변경을 위한 파이썬 파일 
# Unreal에서 나온 데이터를 Mgen 전용으로 segmentation을 재 생성 하는 코드 

import os 
import glob 
import argparse
import cv2
from utils.general import *
from pathlib import Path
import numpy as np 
from tqdm import tqdm
from collections import OrderedDict
def main(opt):
    _label = changeAbsPath(opt.LabelPath,"-lp")
    _image = changeAbsPath(opt.ImagePath,"-ip")
    _labels = check_dir_list(_label,"-lp")
    _refer_Coord = changeAbsPath(opt.ColorCoordinate,"-refer")
    _refer_cls = changeAbsPath(opt.ClassYaml,"-cls_set")
    _refer_color = changeAbsPath(opt.colorSetting,"-colo_set")
    _seg = changeAbsPath(opt.SegImPath,"-sip")
    savepath = path_confirm(opt.SavePath)
    _sr = changeAbsPath(savepath,"-sr")

    newseg = Unreal_dataset(_labels,_seg,_sr,_refer_Coord)
    
def Unreal_dataset(labels,segPath,save_path,refer_coord):
    #print("run")
    # 경로 설정 
    YoloSave = path_confirm(os.path.join(save_path,"YoloForm/")) # "/YoloForm/"으로 하면 M:YoloForm 으로 경로 설정이 되어 버림 이유 모름
    NewSegImgSave= path_confirm(os.path.join(save_path,"MgenFormSegImg/"))
    ConfirmImgSave = path_confirm(os.path.join(save_path,"ConfrimImg/"))
    
    # json
    
    img_coor_json = json_dict(refer_coord)

    for label in tqdm(labels):
        IMAGESUFFIX = [".png",'.jpg','.jpeg']
        i = Path(label)
        s = i.suffix
        
        
        for suf in IMAGESUFFIX:
            n = os.path.join(segPath,os.path.basename(label.replace(s,suf)))
            # print(n)
            if os.path.exists(n):
                imPath = n 
                segName = os.path.basename(imPath)
                label_dict = json_dict(label)
                newSegPath = os.path.join(NewSegImgSave,segName)
                #print(label,imPath)
                if not os.path.exists(newSegPath):
                    seg_path = draw_seg(label_dict,imPath,newSegPath,img_coor_json)
                else:
                    seg_path = newSegPath
                convert_yolo(label_dict,seg_path,yolo_save_root=YoloSave,img_coor_json=img_coor_json)


                
    

            
    
    



def parser_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument("-task","--LabelType",dest = "LabelType",type=str,default="seg",help="[\'seg\',\'bbox\']")
    parser.add_argument("-lp","--LabelPath",dest="LabelPath",type=str,default="./labels",help= "Files(json or txt) directory path")
    parser.add_argument("-ip",'--ImagePath',dest = "ImagePath",type=str,default="./images",help = "Filse (image) directory path")
    
    parser.add_argument("-sip",'--SegImgPath',dest = "SegImPath",type=str,default="./seg",help = "Filse (seg image) directory path")
    parser.add_argument("-refer","--colorCoordinate",dest ="ColorCoordinate",type=str,default="./refer/img_coor.json",help ="Dictionary : Unreal color coordinate")

    # parser.add_argument("-b","--background",dest="backGround",type = str2bool,default=True)
    # parser.add_argument("-lw","--LineWidth",dest="LineWidth",type=float,default=0.3)
    parser.add_argument("-cls_set","--ClassYaml",dest="ClassYaml",type=str,default="./refer/cls.yaml")
    parser.add_argument("-colo_set","--colorSetting",dest ="colorSetting",type=str,default="./refer/color.yaml")
    parser.add_argument("-sr","--saveRoot",dest='SavePath',type=str,default="./result/")
    args = parser.parse_args()
    return parser.parse_known_args()[0] if known else parser.parse_args()



def draw_seg(js,seg,save_root,coor_json):    

    
    car = js["car"]
    cone = js['cone']
    nf = js['nfire']
    fire = "200"
    black_sm = '221'
    gray_sm = '222'
    white_sm = '223'
    
    im = cv2.imread(seg) # ,cv2.IMREAD_REDUCED_COLOR_2
    h,w,c = im.shape
    # 경로상 한글있으면 cv2 못 읽는다. 
    # new_seg_im = np.zeros((int(h),int(w),3),np.uint8)

    object_list = [car,cone,nf]
    
    object_list_cn = ['1','10','14']
    smoke = [black_sm,gray_sm,white_sm]
    smoke_cn = ['4','17','18']
    fire = [fire]
    fire_cn = ['3']
    
    new_seg_im = save_root
    new_im = np.zeros((h,w,c),np.uint8)
    
    img_coor_json = coor_json
    for obj in object_list:
        name,new_seg_im = SetDrawObjectContour(obj,im,img_coor_json,new_im,new_seg_f)
    for sm in smoke:
        name,new_seg_im = SegDrawSmokeFireContour(sm,im,img_coor_json,new_seg_im,new_seg_f)
    for f in fire:
        name,new_seg_im = SegDrawSmokeFireContour(f,im,img_coor_json,new_seg_im,new_seg_f)

    return new_seg_f


def SetDrawObjectContour(coor_id,im,img_coor_json,new_seg_im,name):
   
    if isinstance(coor_id,str):
        pass 
    elif isinstance(coor_id,list):
        for idx in coor_id:
            coor_bgr = list(img_coor_json[str(idx)])
            coor = np.array([coor_bgr[2],coor_bgr[1],coor_bgr[0]],dtype="int64")
            coor_uper = coor+5 
            coor_lower = coor-5
            img_mask = cv2.inRange(im,coor_lower,coor_uper)
            contours, hierachy = cv2.findContours(img_mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
            seg_dict = {}
            cont = []
            if not contours:
                    pass
            for c in contours:
                new_seg_im = cv2.drawContours(new_seg_im,[c],-1,(coor_bgr[2],coor_bgr[1],coor_bgr[0]),-1)
        cv2.imwrite(name,new_seg_im)
    return name, new_seg_im

def SegDrawSmokeFireContour(coor_id,origin_seg,img_coor_json,new_seg,name):
    if isinstance(coor_id,str):
        coor_bgr = list(img_coor_json[str(coor_id)])
        coor = np.array([coor_bgr[2],coor_bgr[1],coor_bgr[0]],dtype="int64")
        coor_uper = coor+5 
        coor_lower = coor-5
        img_mask = cv2.inRange(origin_seg,coor_lower,coor_uper)
        contours, hierachy = cv2.findContours(img_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_KCOS) # cv2.CHAIN_APPROX_TC89_L1 여유롭게 칠함 
        seg_dict = {}
        cont = []
        if not contours:
            pass
        else:
            if len(contours) > 1:
                idx = 0
                m = 0 
                for i,x in enumerate(contours):
                    if m < x.size:
                        m = x.size
                        idx = i
                cont=contours[idx]
            else:
                cont = contours[0]
            epsilon2 = 0.006*cv2.arcLength(cont, True)
            approx1 = cv2.approxPolyDP(cont, epsilon2, True)
            cont = np.vstack((approx1))
            # M = cv2.moments(cont)
            # cx = int(M['m10'] / M['m00'])
            # cy = int(M['m01'] / M['m00'])
            x_contour = cont[:,0] 
            # x_contour[x_contour > cx] += 2
            # x_contour[x_contour < cx] -= 2

            y_contour = cont[:,1] 
            # # y_contour[y_contour > 0] += -5
            # y_contour[y_contour < cy] -= 2
            # y_contour[y_contour > cy] += 2
            if coor_id in ['221','222','223']:
                for i in [2,-2]:
                    x_contours = (x_contour) +i
                    con2 = np.concatenate((x_contours[:,np.newaxis], y_contour[:,np.newaxis]), axis=1)
                    
                    new_seg = cv2.fillPoly(new_seg,[con2],(coor_bgr[2],coor_bgr[1],coor_bgr[0]))
                for i in [2,-2]:
                    y_contours = (y_contour) +i
                    con2 = np.concatenate((x_contours[:,np.newaxis], y_contours[:,np.newaxis]), axis=1)
                    new_seg = cv2.fillPoly(new_seg,[con2],(coor_bgr[2],coor_bgr[1],coor_bgr[0]))
            else:
                for i in [1,-1]:
                    x_contours = (x_contour) +i
                    con2 = np.concatenate((x_contours[:,np.newaxis], y_contour[:,np.newaxis]), axis=1)
                    
                    new_seg = cv2.fillPoly(new_seg,[con2],(coor_bgr[2],coor_bgr[1],coor_bgr[0]))
                for i in [1,-1]:
                    y_contours = (y_contour) +i
                    con2 = np.concatenate((x_contours[:,np.newaxis], y_contours[:,np.newaxis]), axis=1)
                    new_seg = cv2.fillPoly(new_seg,[con2],(coor_bgr[2],coor_bgr[1],coor_bgr[0]))

        cv2.imwrite(name,new_seg)
    return name, new_seg

def convert_yolo(js,segimg,img_coor_json,yolo_save_root):

    
    car = js["car"]
    cone = js['cone']
    nf = js['nfire']
    fire = "200"
    black_sm = '221'
    gray_sm = '222'
    white_sm = '223'

    im = cv2.imread(segimg) # ,cv2.IMREAD_REDUCED_COLOR_2
    h,w,c = im.shape
    obj = [car,cone,nf,black_sm,gray_sm,white_sm,fire]
    cn = ['1','10','14','4','17','18','3']
    # s_obj = [cone,nf,black_sm,gray_sm,white_sm,fire]
    # s_cn = ['10','14','4','17','18','3']
    # obj_car = [car]
    # obj_cn = ['1']

    for o,c in zip(obj,cn):
        

def GetyoloCoordinate(cls,cn,segim,imgcoord,w,h,pixel_threhsold=100):
    def seg_flatten(poly):
        seg = [] 
        for i in poly:
            a = i.flatten()
            
            for j in a:
                j = j# 이미지 1/2배 했을 때 
                seg.append(j)

        return list(map(int, seg))
    result=[]
    if isinstance(cls,str): # fire,smoke
        seg_dict = OrderedDict()
        coord_bgr = list(imgcoord[str(cls)])
        coor = np.array([coord_bgr[2],coord_bgr[1],coord_bgr[0]],dtype="int64")
        contours,_ = cv2.findContours(coor,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_L1)
        print(contours)
        if not contours:
            pass 
        else:
            contList = [] 
            for c in contours:
                area = cv2.contourArea(c)
                if area > pixel_threhsold:
                    cont = np.array(c)
                    contList.append(cont)

            total = [] 
            try:
                if len(contList)<2:
                    for i in cont:
                        z = seg_flatten(i)
                        total.append(z)





if __name__ == "__main__":
    opt = parser_opt(True)
    main(opt)