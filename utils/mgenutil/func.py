import os 
import numpy as np 
import cv2
from ..general import json_dict

def drawSeg(datasets,referCoord,save_root):
   
    refer = json_dict(referCoord)
    segDrawObjectContour(datasets,refer,save_root)
    segDrawSmokeContour(datasets,refer,save_root)
    segDrawFireContour(datasets,refer,save_root)
    

def segDrawObjectContour(datasets,refer,saveroot):
    for data in datasets:
        new_seg = np.zeros(data.getsegImSize(),dtype=np.uint8)  
        dict = data.getcolorInfo()
        for idx,coord in dict.items():
            if isinstance(coord,list):
                for i in coord:
                    coord_bgr = list(refer[str(i)])
                    coor = np.array([coord_bgr[2],coord_bgr[1],coord_bgr[0]],dtype = "int64")
    
                    img_mask = cv2.inRange(data.getsegIm(),coor,coor)
                
                    # print(img_mask)
                    contours,_ = cv2.findContours(img_mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
                    
                    if not contours:
                        pass
                    for c in contours:
                        new_seg= cv2.drawContours(new_seg,[c],-1,(coord_bgr[2],coord_bgr[1],coord_bgr[0]),-1)
                newSegPath = os.path.join(saveroot,data.getImg())
                cv2.imwrite(newSegPath,new_seg)

def segDrawFireContour(datasets,refer,saveroot,fire = True):
    for data in datasets:
        newSegPath = os.path.join(saveroot,data.getImg())
        newSeg = cv2.imread(newSegPath)
        dict = data.getcolorInfo()
        for idx,coord in dict.items():
            if isinstance(coord,str) and fire:
                coord_bgr = list(refer[str(coord)])
                coor = np.array([coord_bgr[2],coord_bgr[1],coord_bgr[0]],dtype = "int64")
                #print(coor)
                img_mask = cv2.inRange(data.getsegIm(),coor,coor)
                # print(img_mask)
                contours,_ = cv2.findContours(img_mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
                if not contours:
                    pass
                for c in contours:
                    new_seg= cv2.drawContours(newSeg,[c],-1,(coord_bgr[2],coord_bgr[1],coord_bgr[0]),-1)
                # cv2.imshow("fire",new_seg)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                cv2.imwrite(newSegPath,new_seg)
    return newSegPath

def segDrawSmokeContour(datasets,refer,saveroot,epsilon = 0.006,extra_pixels = 1):
    for data in datasets:
        newSegPath = os.path.join(saveroot,data.getImg())
        newSeg = cv2.imread(newSegPath)
        dict = data.getcolorInfo()
        for idx,coord in dict.items():
            if isinstance(coord,str) and idx !="fire":
                coord_bgr = list(refer[str(coord)])
                coor = np.array([coord_bgr[2],coord_bgr[1],coord_bgr[0]],dtype = "int64")

                img_mask = cv2.inRange(data.getsegIm(),coor,coor)

                contours,_ = cv2.findContours(img_mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
                if not contours:
                    pass
                    
                else:
                    if len(contours) >1:
                        idx = 0
                        m = 0 
                        for i,x in enumerate(contours):
                            if m < x.size:
                                m = x.size
                                idx = i 
                        cont = contours[idx]
                    else:
                        cont = contours[0]
                    epislon2 = epsilon*cv2.arcLength(cont,True)
                    approx1 = cv2.approxPolyDP(cont,epislon2,True)
                    cont = np.vstack((approx1))
                    x_contour = cont[:,0]
                    y_contour = cont[:,1]

                    if coord in ["221","222","223"]:
                        for i in [extra_pixels,-extra_pixels]:
                            x_contours = (x_contour) + i 
                            con2 = np.concatenate((x_contours[:,np.newaxis],y_contours[:,np.newaxis]),axis=1)
                            new_seg = cv2.fillPoly(new_seg,[con2],(coord_bgr[2],coord_bgr[1],coord_bgr[0]))
                        for i in [extra_pixels,-extra_pixels]:
                            y_contours = (y_contour) + i
                            con2 = np.concatenate((x_contours[:np.newaxis],y_contours[:,np.newaxis]),axis=1)
                            new_seg = cv2.fillPoly(new_seg,[con2],(coord_bgr[2],coord_bgr[1],coord_bgr[0]))

                    else:
                        


                for c in contours:
                    new_seg= cv2.drawContours(newSeg,[c],-1,(coord_bgr[2],coord_bgr[1],coord_bgr[0]),-1)

                cv2.imwrite(newSegPath,new_seg)
    return newSegPath

