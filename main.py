import os 
import shutil
import glob

import time
from utils import *
try:
    from PIL import Image
    import cv2 
except:
    os.system("pip install pillow")
    os.system("pip install opencv-python")
    from PIL import Image
    import cv2 
    
def main():
    img_coor_json = json_dict("./refer/img_coor.json")
    data_json = glob.glob("./json/*")
    read_seg = glob.glob("./seg/*")

    
    yolo_label_dir = path_confirm("./yolo/")
    new_seg_folder = path_confirm("./fire_smoke_new_seg_im/")
    confirm_img_seg = path_confirm("./convert_confirm/")
    for i in read_seg:
        n = os.path.basename(i)
        shutil.copy2(i,os.path.join(new_seg_folder,n))
    print('copy_complet')
    for js in data_json:
        # start = time.time()
        d = draw_seg(js,new_seg_folder,img_coor_json)
        cy = convert_yolo(js,img_coor_json,yolo_label_dir)
        cc = convert_confirm(cy,confirm_img_seg,yolo_label_dir)
        # end = time.time()
        # print(f"{end - start:.5f} sec")

def convert_confirm(f,save_path,yolo_label_dir,w=1920,h=1080):
    img = os.path.join("./train/images/",os.path.basename(f).replace(".txt",".png"))
    gt = os.path.join(yolo_label_dir,f)

    im = Image.open(img)
    confirm_seg(im,gt,w,h,save_path)

def convert_yolo(js,img_coor_json,yolo_seg_root):
    seg_ls = []
    root = os.path.dirname(js)
    im_root = root.replace('json','fire_smoke_new_seg_im') # read ./seg  
    name = os.path.basename(js) # name.json

    im_name = name.replace(".json",".png") # name.png
    file_name = name.replace(".json",".txt") # name.txt

    read_seg_file = os.path.join(im_root,im_name) # seg image 

    j = json_dict(js)
    car = j["car"]
    cone = j['cone']
    nf = j['nfire']
    fire = "200"
    black_sm = '221'
    gray_sm = '222'
    white_sm = '223'

    im = cv2.imread(read_seg_file) # ,cv2.IMREAD_REDUCED_COLOR_2
    h,w,c = im.shape
    
    obj = [cone,nf,black_sm,gray_sm,white_sm,fire]
    cn = ['10','14','4','17','18','3']
    obj_car = [car]
    obj_cn = ['1']

    for o,c in zip(obj,cn):
        one_list = Getyolo_seg(o,c,im,img_coor_json,w,h,pixcel_threshold=200)
        seg_ls.extend(one_list)
    for o,c in zip(obj_car,obj_cn):
        one_list = Getyolo_seg_car(o,c,im,img_coor_json,w,h)
        seg_ls.extend(one_list)

    n = save_txt(yolo_seg_root,seg_ls,file_name)
    return n

def draw_seg(js,new_seg_folder,img_coor_json):    
    
    root = os.path.dirname(js)
    im_root = root.replace('json','seg') # read ./seg  
    name = os.path.basename(js) # name.json

    im_name = name.replace(".json",".png") # name.png
    

    read_seg_file = os.path.join(im_root,im_name) # seg image 

    j = json_dict(js)
    car = j["car"]
    cone = j['cone']
    nf = j['nfire']
    fire = "200"
    black_sm = '221'
    gray_sm = '222'
    white_sm = '223'

    im = cv2.imread(read_seg_file) # ,cv2.IMREAD_REDUCED_COLOR_2
    h,w,c = im.shape
    # new_seg_im = np.zeros((int(h),int(w),3),np.uint8)

    object_list = [car,cone,nf]
    object_list_cn = ['1','10','14']
    smoke = [black_sm,gray_sm,white_sm]
    smoke_cn = ['4','17','18']
    fire = [fire]
    fire_cn = ['3']
    
    new_seg_f = os.path.join(new_seg_folder,im_name)
    new_seg_im = cv2.imread(new_seg_f)

    for obj in object_list:
        name,new_seg_im = SetDrawObjectContour(obj,im,img_coor_json,new_seg_im,new_seg_f)
    for sm in smoke:
        name,new_seg_im = SegDrawSmokeFireContour(sm,im,img_coor_json,new_seg_im,new_seg_f)
    for f in fire:
        name,new_seg_im = SegDrawSmokeFireContour(f,im,img_coor_json,new_seg_im,new_seg_f)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"{end - start:.5f} sec")