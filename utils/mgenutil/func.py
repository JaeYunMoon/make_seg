import os 
import numpy as np 
import cv2
from ..general import json_dict,logger

def drawSeg(datasets,referCoord,save_root,txtSaveRoot):
   
    refer = json_dict(referCoord)
    segDrawObjectContour(datasets,refer,save_root,txtSaveRoot)
    segDrawFireSmokeContour(datasets,refer,save_root,fire=False)
    segDrawFireSmokeContour(datasets,refer,save_root,fire = True)
    YoloConvertFireSmoke(datasets,refer,txtSaveRoot)
    

def segDrawObjectContour(datasets,refer,saveroot,txtSavePath):
    for data in datasets:
        segments =[]
        new_seg = np.zeros(data.getsegImSize(),dtype=np.uint8)  
        dict = data.getcolorInfo()
        clsdict = {v.lower():k for k,v in data.clsInfo.items()}
        h,w,c = data.getsegImSize()
        for idx,coord in dict.items():
            if isinstance(coord,list):
                for i in coord:
                    contour_merge = []
                    coord_bgr = list(refer[str(i)])
                    coor = np.array([coord_bgr[2],coord_bgr[1],coord_bgr[0]],dtype = "int64")
    
                    img_mask = cv2.inRange(data.getsegIm(),coor,coor)
                
                    # print(img_mask)
                    contours,_ = cv2.findContours(img_mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
                    
                    if not contours:
                        pass
                    for c in contours:
                        new_seg= cv2.drawContours(new_seg,[c],-1,(coord_bgr[2],coord_bgr[1],coord_bgr[0]),-1)
                        
                        s = seg_flatten(c)
                        contour_merge.append(s)
                        if len(contour_merge) >1:
                            if len(contour_merge) > 2:
                                logger.info(f"동일 객체 3등분 {data.getImg()} {idx}")
                            s1 = merge_multi_segment(contour_merge)
                            
                            s1 = (np.concatenate(s1,axis=0) / np.array([w,h])).reshape(-1).tolist()
                        else:
                            s1 = (j for i in contour_merge for j in i)
                            s1 = (np.array(list(s1)).reshape(-1,2)/np.array([w,h])).reshape(-1).tolist()

                        s1 = [idx]+s1
                        if s1 not in segments:
                            segments.append(s1)

                newSegPath = os.path.join(saveroot,data.getImg())
                cv2.imwrite(newSegPath,new_seg)
            
                txtPath = os.path.join(txtSavePath,data.getYoloName())
                with open(txtPath,"w") as f:
                    for s in segments:
                        ind,*seg = s
                        cls = clsdict[ind]
                        f.write(f"{cls} ")
                        for x in seg:
                            x = float(x)
                            f.write(f"{x} ")
                        f.write("\n")
                    
def segDrawFireSmokeContour(datasets,refer,saveroot,fire = True):
    for data in datasets:
        newSegPath = os.path.join(saveroot,data.getImg())
        newSeg = cv2.imread(newSegPath)
        dict = data.getcolorInfo()
        contours = None
        for idx,coord in dict.items():
            if fire and isinstance(coord,str) and idx == "fire":
                coord_bgr = list(refer[str(coord)])
                segFindandDraw(data,newSeg,newSegPath,coord,coord_bgr)
                
            elif not fire and isinstance(coord,str) and idx !="fire":
                coord_bgr = list(refer[str(coord)])
                segFindandDraw(data,newSeg,newSegPath,coord,coord_bgr)

def segFindandDraw(data,newSeg,newSegPath,coord,coordbgr,epsilon = 0.0006,extra_pixels = 1):
    coor = np.array([coordbgr[2],coordbgr[1],coordbgr[0]],dtype="int64")
    img_mask = cv2.inRange(data.getsegIm(),coor,coor)
    contours,_=cv2.findContours(img_mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        pass 
    else:
        if len(contours) > 1: # 가장 큰 연기 or 불만 잡는 조건문 
            idx = 0
            m = 0 
            for i,x in enumerate(contours):
                if m < cv2.contourArea(x):
                    m = cv2.contourArea(x)
                    idx = i 
            cont = contours[idx] 
        else:
            cont = contours[0]
        epsilon2 = epsilon*cv2.arcLength(cont,True)
        approx1 = cv2.approxPolyDP(cont,epsilon2,True)
        cont = np.vstack((approx1))
        x_contour = cont[:,0]
        y_contour = cont[:,1]

        if coord in ["221","222","223"]:
            for i in [extra_pixels,-extra_pixels]:
                x_contours = (x_contour) + i 
                con2 = np.concatenate((x_contours[:,np.newaxis], y_contour[:,np.newaxis]), axis=1)
                newSeg = cv2.fillPoly(newSeg,[con2],(coordbgr[2],coordbgr[1],coordbgr[0]))
            for i in [extra_pixels,-extra_pixels]:
                y_contours = (y_contour) + i
                con2 = np.concatenate((x_contours[:,np.newaxis], y_contours[:,np.newaxis]), axis=1)
                newSeg = cv2.fillPoly(newSeg,[con2],(coordbgr[2],coordbgr[1],coordbgr[0]))

        else:
            for i in [extra_pixels,-extra_pixels]:
                x_contours = (x_contour) +i
                con2 = np.concatenate((x_contours[:,np.newaxis], y_contour[:,np.newaxis]), axis=1)
                
                newSeg = cv2.fillPoly(newSeg,[con2],(coordbgr[2],coordbgr[1],coordbgr[0]))
            for i in [extra_pixels,-extra_pixels]:
                y_contours = (y_contour) +i
                con2 = np.concatenate((x_contours[:,np.newaxis], y_contours[:,np.newaxis]), axis=1)
                newSeg = cv2.fillPoly(newSeg,[con2],(coordbgr[2],coordbgr[1],coordbgr[0]))


    for c in contours:
        newSeg= cv2.drawContours(newSeg,[c],-1,(coordbgr[2],coordbgr[1],coordbgr[0]),-1)

    cv2.imwrite(newSegPath,newSeg)




def seg_flatten(poly):
    seg = [] 
    for i in poly:
        a = i.flatten()
        
        for j in a:
            j = j# 이미지 1/2배 했을 때 
            seg.append(j)

    return [int(x) for x in seg]

def min_index(arr1, arr2):
    dis = ((arr1[:, None, :] - arr2[None, :, :]) ** 2).sum(-1)
    print(dis)
    return np.unravel_index(np.argmin(dis, axis=None), dis.shape)

def merge_multi_segment(segments):
    """
    Merge multi segments to one list. Find the coordinates with min distance between each segment, then connect these
    coordinates with one thin line to merge all segments into one.

    Args:
        segments(List(List)): original segmentations in coco's json file.
            like [segmentation1, segmentation2,...],
            each segmentation is a list of coordinates.
    """
    s = []
    segments = [np.array(i).reshape(-1, 2) for i in segments]
    idx_list = [[] for _ in range(len(segments))]

    # record the indexes with min distance between each segment
    for i in range(1, len(segments)):
        idx1, idx2 = min_index(segments[i - 1], segments[i])
        idx_list[i - 1].append(idx1)
        idx_list[i].append(idx2)

    # use two round to connect all the segments
    for k in range(2):
        # forward connection
        if k == 0:
            for i, idx in enumerate(idx_list):
                # middle segments have two indexes
                # reverse the index of middle segments
                if len(idx) == 2 and idx[0] > idx[1]:
                    idx = idx[::-1]
                    segments[i] = segments[i][::-1, :]

                segments[i] = np.roll(segments[i], -idx[0], axis=0)
                segments[i] = np.concatenate([segments[i], segments[i][:1]])
                # deal with the first segment and the last one
                if i in [0, len(idx_list) - 1]:
                    s.append(segments[i])
                else:
                    idx = [0, idx[1] - idx[0]]
                    s.append(segments[i][idx[0] : idx[1] + 1])

        else:
            for i in range(len(idx_list) - 1, -1, -1):
                if i not in [0, len(idx_list) - 1]:
                    idx = idx_list[i]
                    nidx = abs(idx[1] - idx[0])
                    s.append(segments[i][nidx:])
    return s

def YoloConvertFireSmoke(datasets,refer,saveroot):
    
    for data in datasets:
        segments =[]
        new_seg = np.zeros(data.getsegImSize(),dtype=np.uint8)  
        dict = data.getcolorInfo()
        clsdict = {v.lower():k for k,v in data.clsInfo.items()}
        #print(clsdict)
        h,w,c = data.getsegImSize()
        for cls,coord in dict.items():
            
            if isinstance(coord,str):

                #print(cls)
                merge_contour = [] 
                coord_bgr = list(refer[str(coord)])
                coor = np.array([coord_bgr[2],coord_bgr[1],coord_bgr[0]],dtype="int64")
                img_mask = cv2.inRange(data.getsegIm(),coor,coor)
                contours,_=cv2.findContours(img_mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
                if not contours:
                    pass 
                else:
                    if len(contours) > 1: # 가장 큰 연기 or 불만 잡는 조건문
                        if len(contours) > 2:
                            logger.info(f"동일 객체 3등분 {data.getImg()} {cls}")
                        idx = 0
                        m = 0 
                        for i,x in enumerate(contours):
                            if m < cv2.contourArea(x):
                                m = cv2.contourArea(x)
                                idx = i 
                        contour = contours[idx]
                    else:
                        contour = contours

                    s = [seg_flatten(contour)]
                    s1 = (j for i in s for j in i)
                    s1 = (np.array(list(s1)).reshape(-1,2)/np.array([w,h])).reshape(-1).tolist()
                    s1 = [cls]+s1
                    #print(cls)
                    #print(s1)
                    
                    if s1 not in segments:
                        segments.append(s1)
                            
        txtPath = os.path.join(saveroot,data.getYoloName())
        with open(txtPath,"r") as f:
            lines = f.readlines()
        
        with open(txtPath,"w") as f:
            for l in lines:
                f.write(l)
            for s in segments:
                ind,*seg = s
                #print(ind)
                cls = clsdict[ind]
                f.write(f"{cls} ")
                for x in seg:
                    x = float(x)
                    f.write(f"{x} ")
                f.write("\n")

                    