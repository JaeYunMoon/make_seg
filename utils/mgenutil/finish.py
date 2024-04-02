import os 
import shutil
from ..general import path_confirm,json_dict
import cv2 
import numpy as np 
from tqdm import tqdm
from typing import List
import glob 

# origin 과 confrim image file list를 읽어와서 
# 없는 것들은 remove.txt 파일에 쓰고, 라인 확인 후 차이 맞으면 
# 해당 txt 파일에 있는 image파일 삭제 or move 

def compare_and_record(folder1, folder2, output_file):
    # 폴더 1과 폴더 2에서 파일 목록 가져오기
    files_folder1 = set(os.listdir(folder1))
    files_folder2 = set([os.path.basename(x).replace(".txt","") for x in glob.glob(folder2+"/*.png")])

    print(len(files_folder1))
    print(len(files_folder2))
    # 두 목록을 비교하여 한쪽에만 있는 파일 찾기
    unique_files = (files_folder1 - files_folder2).union(files_folder2 - files_folder1)
    
    # 결과를 txt 파일에 기록
    with open(output_file, 'w') as file:
        for file_name in unique_files:
            file.write(file_name + '\n')
    
    print(f"{len(unique_files)} 개의 고유 파일이 {output_file}에 기록되었습니다.")
    
    return output_file

def moveFile(folder1,txtFile,move,saveRoot,name,suffix=".png"):
    with open(txtFile, 'r') as file:
        files_to_delete = file.read().splitlines()
    if not files_to_delete:
        print(f"Remove {name} File not exist")
    else:
        key_pressed = ""
        while key_pressed.upper not in ["Y","N"]:

            print(f"Check the contents of the fileFile checking {txtFile}")
            print(f"\'Y\' to Move == {move} if True = save {saveRoot}, elif False = remove")
            print(f"\'N\' to Stop")
            key_pressed = input("")
            
            if str(key_pressed).upper() == "Y":
                break
            elif str(key_pressed).upper() == "N":
                raise Exception("Input \'N\'")
        
        
        if move:
            move_save = path_confirm(f"{saveRoot}/removeFile/{name}/")
            print(f"MoveDirectorys : {move_save}",)
        deleted_files_count = 0 
        for file_name in tqdm(files_to_delete,desc="File removimg :"):
            file_name = file_name.replace(".png",suffix)
            file_path = os.path.join(folder1, file_name)
            if os.path.exists(file_path):
                if move:
                    shutil.move(file_path,os.path.join(move_save,file_name))
                elif not move:
                    os.remove(file_path)
                deleted_files_count += 1
            else:
                print(f"File not found: {file_path}")
        print(f"Total deleted files: {deleted_files_count}")

def chromaGenerating(imgs,segPath,savePath,_refer):
    smoke = ["221","222","223"]
    fire = "200"
    segP = newSegImage(segPath,savePath,_refer,fire)
    segP = newSegImage(segPath,savePath,_refer,smoke)
    

    for img in tqdm(imgs,desc="Generating Chroma"):
        n = os.path.basename(img)
        # print(segP)
        sg = os.path.join(segP,n)
        Im = cv2.imread(img,cv2.IMREAD_COLOR)
        #print(img)
        segIm = cv2.imread(sg,cv2.IMREAD_COLOR)
        saveName = os.path.join(savePath,n)

        cIm = Im.copy()
        removeBackground = np.dstack((cIm,np.ones((segIm.shape[:-1]))*255))
        segRgba = np.dstack((segIm,np.ones((segIm.shape[:-1]))*255))

        blue,green,red,alpha = segRgba[:,:,0], segRgba[:,:,1],segRgba[:,:,2],segRgba[:,:,3]

        mask1 = (red == 107) & (green == 68) & (blue == 190) & (alpha == 255)   
        mask2 = (red == 210) & (green == 96) & (blue == 94) & (alpha == 255)    
        mask3 = (red == 123) & (green == 48) & (blue == 18) & (alpha == 255)
        mask4 = (red == 137) & (green == 197) & (blue == 162) & (alpha == 255)
        mask = (mask1 | mask2 | mask3 | mask4)

        removeBackground[:,:,:4][np.invert(mask)] = [0, 0, 0, 0]
        cv2.imwrite(saveName,removeBackground)

        
def newSegImage(segPath,savePath,_refer,coord):
    def drawnewSeg(segIm,coordbgr,savePath,zeroIm,fire = True):
        coor = np.array([coordbgr[2],coordbgr[1],coordbgr[0]],dtype="int64")
        img_mask = cv2.inRange(segIm,coor,coor)
        contours,_=cv2.findContours(img_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        if not contours and not os.path.exists(savePath):
            cv2.imwrite(savePath,zeroIm)
            return savePath 
        elif not contours and os.path.exists(savePath):
            return 
        else:
            if len(contours) >1:
                idx = 0 
                m = 0 
                for i,x in enumerate(contours):
                    if m < cv2.contourArea(x):
                        m = cv2.contourArea(x)
                        idx = i 
                cont = [contours[idx]]
            else:
                cont = contours 

        if fire: 
            new = cv2.drawContours(zeroIm,cont,-1,(coordbgr[2],coordbgr[1],coordbgr[0]),-1)
            cv2.imwrite(savePath,new)
        else:
            if os.path.exists(savePath):
                sIm = cv2.imread(savePath)
            else:
                sIm = zeroIm
            new = cv2.drawContours(sIm,cont,-1,(coordbgr[2],coordbgr[1],coordbgr[0]),-1)
            cv2.imwrite(savePath,new)
        return savePath
    sp = os.path.dirname(savePath)
    sp = os.path.join(sp,"FinalSegmentation/")
    if not os.path.exists(sp):
        os.makedirs(sp)
    files_folder1 = glob.glob(segPath+"/*.png")

    _refer = json_dict(_refer)
    for f in tqdm(files_folder1,desc=f"Create segmentation image for chroma productionCroma Generating in {sp}"):
        fim = cv2.imread(f)
        zeros = np.zeros(fim.shape,dtype=np.uint8)
        
        n = os.path.basename(f)
        _savepath = os.path.join(sp,n)

        if isinstance(coord,str):
            coordbgr = list(_refer[str("200")])
            sr = drawnewSeg(fim,coordbgr,savePath=_savepath,zeroIm=zeros,fire=True)
        elif isinstance(coord,list):
            for coo in coord:
                coordbgr = list(_refer[str(coo)])
                sr = drawnewSeg(fim,coordbgr,_savepath,zeros,fire=False)



    return sp