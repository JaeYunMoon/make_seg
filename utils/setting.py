import os
import re 
from collections import defaultdict
from pathlib import Path
from .general import TxtRead,checkLabelSuffix,LabelFormat,json_dict,yaml_dict


try:
    from PIL import Image
    import cv2 
    
    import yaml
    
except:
    os.system("pip install pillow")
    os.system("pip install opencv-python")
    from PIL import Image
    import cv2 

IMAGE_FORMAT = [".png",".jpg",".jpeg"]

def getDatasets(labels,
                imgPath,
                clsYaml,
                refer,
                setting_color,
                new_seg,
                allDataset = None,
                ):
    
    if allDataset is None:
        allDataset = allDatasets()

    for l in labels:
        labelPath = Path(l)
        labelName = os.path.basename(l)
        labelSuffix = labelPath.suffix
        labelType = checkLabelSuffix(labelSuffix)
        for ip in IMAGE_FORMAT:
            n = os.path.join(imgPath,labelName.replace(labelSuffix,ip))
            if os.path.exists(n):
                imagePath = n
        

        if new_seg:
            pass 
        else:
            data = getDataInfo(
                labelPath,
                labelType,
                imagePath,
                clsYaml,
                refer,
                setting_color,
                ns = 0
            )
            


        
        allDataset.addData(data)
    return allDataset
            
    


class getDataInfo():
    def __init__(self,
                 LabelPath,
                 LabelType,
                 ImagePath,
                 clsYaml,
                 coordrefer,
                 setting_color,
                 ns = 0
                 ) -> None:
        self.labelPath = LabelPath
        self.labelType = LabelType
        self.referCoord = coordrefer
        self.clsYaml = clsYaml
        self.Image = ImagePath
        self.settingcolor = setting_color
        self.ns = ns
    def getImTitle(self):
        return os.path.basename(self.labelPath)
    def getrefer(self):
        return json_dict(self.referCoord)
    
    def getclsDict(self):
        return yaml_dict(self.clsYaml)
    
    def getSettingColor(self):
        return yaml_dict(self.settingcolor)
            
    def getIm(self):
        im = Image.open(self.Image)
        return im

    def getImageSize(self):
        img = self.getIm()
        w,h = img.size
        return w,h  
    
    def getLabelInfo(self): #segmentation만 적용 
        objDict = defaultdict(list)
        if self.labelType == LabelFormat.TXTForm:
            objs = TxtRead(self.labelPath)
            for obj in objs:
                for ob in obj:
                    c,*segcoord = ob.strip().split(" ")
                    segcoord = [float(re.sub("[^0-9.]","",c)) for c in segcoord]
                    objDict[c].append(segcoord)
            
            return objDict
        elif self.labelType == LabelFormat.JsonForm:
            pass
        else:
            pass

        
class allDatasets:
    def __init__(self) -> None:
        self._data=[]
    
    def addData(self,data):
        self._data.append(data)
    
    def removeAllData(self):
        self._data = []

    def getDataset(self):
        return self._data

