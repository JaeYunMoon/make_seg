import os
from pathlib import Path
from .general import TxtRead
try:
    from PIL import Image
    import cv2 
    from easydict import EasyDict as edict
    from enum import Enum
except:
    os.system("pip install pillow")
    os.system("pip install easydict")
    os.system("pip install opencv-python")
    from PIL import Image
    import cv2 

class getDataInfo():
    def __init__(self,
                 labelsPath,
                 ImagePath,
                 ) -> None:
        self.imageFormat = [".png",".jpg",".jpeg"]
        self.labelPath = labelsPath
        self.ImgPath = ImagePath

    def getLabelType(self):
        suf = Path(self.labelPath).suffix
        if suf == ".txt":
            return LabelFormat.TxtForm
        elif suf ==".json":
            return LabelFormat.JsonForm 
        else:
            raise TypeError
        
    def getImageName(self):
        n = os.path.basename(self.labelPath)
        im_path = None
        imName = None
        if self.getLabelType() == LabelFormat.TxtForm:
            for i in self.imageFormat:
                imName = n.replace(".txt",i)
                path =os.path.join(self.ImgPath,imName)
                if os.path.exists(path):
                    im_path = path
            return im_path
                
        elif self.getLabelType() == LabelFormat.JsonForm:
            for i in self.imageFormat:
                imName = n.replace(".json",i)
                path =os.path.join(self.ImgPath,imName)
                if os.path.exists(path):
                    im_path = path
            return im_path
                
            
    def getIm(self):
        imPath = self.getImageName()
        im = Image.open(imPath)
        return im
    
    def getImageSize(self):
        img = self.getIm()
        w,h = img.size
        return w,h  
    
    def getLabelInfo(self):
        if self.getLabelType() == LabelFormat.TxtForm:
            return TxtRead(self.labelPath)
    


class LabelFormat(Enum):
    TxtForm = 1
    JsonForm =2 