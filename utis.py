import os 
import re
from collections import OrderedDict
from pathlib import Path 
import numpy as np 
import cv2
import json

try:
    import matplotlib.pyplot as plt 
    import matplotlib.image as img
    from matplotlib.patches import Polygon
    from matplotlib.collections import PatchCollection
    from easydict import EasyDict as edict
except:
    os.system("pip install easydict")
    os.system("pip install matplotlib")
    from easydict import EasyDict as edict
    import matplotlib.pyplot as plt 
    import matplotlib.image as img
    from matplotlib.patches import Polygon
    from matplotlib.collections import PatchCollection


def json_dict(jpth):
    with open(jpth,"r",encoding="cp949") as f:
        js_file = edict(json.load(f))
    return js_file

def confirm_seg(im,gt,w,h,save_root): 
    plt.imshow(im);plt.axis("off")
    ax = plt.gca()
    polygons = [] 
    color = [] 
    title = Path(gt).name
    with open(gt,"r") as f:
        data_info = f.readlines()
    for di in data_info:
        ls = [d for d in di.strip().split(" ")]
        coo = [re.sub("[^0-9.]","",x) for x in ls[1:]]
        coor = [float(x) for x in coo]
        c = (np.random.random((1, 3))*0.6+0.4).tolist()[0]

        poly = np.array(coor,dtype=np.float32).reshape((int(len(coor)/2),2))
        poly[:,:1] = poly[:,:1]*w
        poly[:,1:] = poly[:,1:]*h 
        polygons.append(Polygon(poly))
        color.append(c)
    p = PatchCollection(polygons, facecolor=color, linewidths=0, alpha=0.4)
    ax.add_collection(p)
    p = PatchCollection(polygons, facecolor='none', edgecolors=color, linewidths=0.3)
    ax.add_collection(p)

    plt.title(str(title))
    save = os.path.join(save_root,f"{str(title)}_seg.png")
    
    plt.savefig(save,bbox_inches='tight', pad_inches=0,dpi = 300)
    plt.clf()
    return save

def seg_flatten(poly):
    seg = [] 
    for i in poly:
        a = i.flatten()
        
        for j in a:
            j = j# 이미지 1/2배 했을 때 
            seg.append(j)

    return list(map(int, seg))

def seg_array(poly,w,h):
    # 한번에 라벨링 
    new_polygons = []
    for p in poly:
        new_polygon = np.array([[x,y] for x,y in zip(p[0::2],p[1::2])],dtype=float)
        #print("new_poly",new_poly)
        new_polygon[:,0] = new_polygon[:,0]/(w)
        new_polygon[:,1] = new_polygon[:,1]/(h)
        new_polygons.extend(new_polygon.reshape(-1)) 
    return new_polygons

def save_txt(save_path,ls,file_name,seg_bool = False):
    if not seg_bool:
        with open(save_path+file_name,'w',encoding="utf-8") as f:
            for i in ls:
                for ind,val in i.items():
                    f.write(f"{ind} ")
                    for index in range(len(val)):
                        f.write(f"{val[index]} ")
                    f.write("\n")
            f.close()
    return file_name

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


def GetFireContour(coor_id,origin_seg,img_coor_json,new_seg,name):
    if isinstance(coor_id,str):
        coor_bgr = list(img_coor_json[str(coor_id)])
        coor = np.array([coor_bgr[2],coor_bgr[1],coor_bgr[0]],dtype="int64")
        coor_uper = coor+5 
        coor_lower = coor-5
        img_mask = cv2.inRange(origin_seg,coor_lower,coor_uper)
        contours, hierachy = cv2.findContours(img_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_L1) # cv2.CHAIN_APPROX_TC89_L1 여유롭게 칠함 
        seg_dict = {}
        cont = []
        if not contours:
            pass
        else:
            if len(contours) > 1:
                idx = 0
                m = 0 
                sidx = 0
                sm = 0
                for i,x in enumerate(contours):
                    if m < x.size:
                        x = x.size
                        idx = i
                cont=contours[idx]
                
            else:
                cont = contours[0]
        new_seg = cv2.drawContours(new_seg,[cont],-1,(coor_bgr[2],coor_bgr[1],coor_bgr[0]),-1)
        cv2.imwrite(name,new_seg)
    return name, new_seg

def Getyolo_seg(coor_id,cn,seg_im,img_coor_json,w,h,pixcel_threshold=100):
    return_list = [] 
    
    if isinstance(coor_id,str):
        seg_dict = OrderedDict()
        coor_bgr = list(img_coor_json[str(coor_id)])
        coor = np.array([coor_bgr[2],coor_bgr[1],coor_bgr[0]],dtype="int64")
        coor_uper = coor+5 
        coor_lower = coor-5
        # 이미지에서 해당 객체의 세그멘테이션 정보 추출
        img_mask = cv2.inRange(seg_im,coor_lower,coor_uper)
        contours, hierachy = cv2.findContours(img_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_L1)
        
        if not contours:
            pass 
        else:
            cont_ls = [] 
            for x in contours:
                area = cv2.contourArea(x)
                if area > pixcel_threshold:
                    cont=np.array(x)
                    cont_ls.append(cont)
            total = []
            try:
                if len(cont_ls) < 2: 
                    for i in cont:
                        z = seg_flatten(i)
                        total.append(z)
                else:
                    for i in cont_ls:
                        for j in i:
                            z = seg_flatten(i)
                            total.append(z)

                seg_dict[str(cn)] = seg_array(total,w,h)
                
                return_list.append(seg_dict)
            except:
                pass 
    
    elif isinstance(coor_id,list):
        for i in coor_id:
            seg_dict = OrderedDict()
            coor_bgr = list(img_coor_json[str(i)])
            coor = np.array([coor_bgr[2],coor_bgr[1],coor_bgr[0]],dtype="int64")
            coor_uper = coor+5 
            coor_lower = coor-5
            # 이미지에서 해당 객체의 세그멘테이션 정보 추출
            img_mask = cv2.inRange(seg_im,coor_lower,coor_uper)
            contours, hierachy = cv2.findContours(img_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_L1)
            if not contours:
                pass
            else:
                total = []
                for i in contours:
                    z = seg_flatten(i)
                    total.append(z)

                seg_dict[str(cn)] = seg_array(total,w,h)
                return_list.append(seg_dict)
    return return_list

def Getyolo_seg_car(coor_id,cn,seg_im,img_coor_json,w,h,pixcel_threshold = 300):
    return_list = [] 
    
    if isinstance(coor_id,str):
        
        seg_dict = OrderedDict()
        coor_bgr = list(img_coor_json[str(coor_id)])
        coor = np.array([coor_bgr[2],coor_bgr[1],coor_bgr[0]],dtype="int64")
        coor_uper = coor+5 
        coor_lower = coor-5
        # 이미지에서 해당 객체의 세그멘테이션 정보 추출
        img_mask = cv2.inRange(seg_im,coor_lower,coor_uper)
        contours, hierachy = cv2.findContours(img_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_L1)
        if not contours:
            pass 
        else:
            cont_ls = [] 
            for x in contours:
                area = cv2.contourArea(x)
                if area > pixcel_threshold:
                    cont=np.array(x)
                    cont_ls.append(cont)
            total = []
            try:
                if len(cont_ls) < 2: 
                    for i in cont:
                        z = seg_flatten(i)
                        total.append(z)
                else:
                    for i in cont_ls:
                        for j in i:
                            z = seg_flatten(i)
                            total.append(z)

                seg_dict[str(cn)] = seg_array(total,w,h)
                
                return_list.append(seg_dict)
            except:
                pass 
        
    elif isinstance(coor_id,list):
        
        for i in coor_id:
            seg_dict = OrderedDict()
            coor_bgr = list(img_coor_json[str(i)])
            coor = np.array([coor_bgr[2],coor_bgr[1],coor_bgr[0]],dtype="int64")
            coor_uper = coor+5 
            coor_lower = coor-5
            # 이미지에서 해당 객체의 세그멘테이션 정보 추출
            img_mask = cv2.inRange(seg_im,coor_lower,coor_uper)
            contours, hierachy = cv2.findContours(img_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_L1)
            if not contours:
                pass 
            else:
                cont_ls = [] 
                for x in contours:
                    area = cv2.contourArea(x)
                    if area > pixcel_threshold:
                        cont=np.array(x)
                        cont_ls.append(cont)
                total = []
                try:
                    if len(cont_ls) < 2: 
                        for i in cont:
                            z = seg_flatten(i)
                            total.append(z)
                    else:
                        for i in cont_ls:
                            for j in i:
                                z = seg_flatten(i)
                                total.append(z)

                    seg_dict[str(cn)] = seg_array(total,w,h)
                    
                    return_list.append(seg_dict)
                except:
                    pass 
    return return_list

# def GetObjectContour_smoke(coor_id,im,img_coor_json):
#     pass
def path_confirm(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path        

   
