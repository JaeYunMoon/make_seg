import os 
from pathlib import Path
import cv2
from PIL import Image
from ..general import checkLabelSuffix,LabelFormat,json_dict,TxtRead,yaml_dict



IMAGE_FORMAT = [".png",".jpg",".jpeg"]

def getDatasets(
        labels,
        imgPath,
        segImgPath,
        clsInfo,
        colrInfo,
        unrealoutput = None
):
    if unrealoutput == None:
        unrealoutput = allUnreal()

    for label in labels:
        labelPath = Path(label)
        labelName = os.path.basename(label)
        labelSuffix = labelPath.suffix
        labelType = checkLabelSuffix(labelSuffix)
        imagePath = None

        for ip in IMAGE_FORMAT:
            n = os.path.join(segImgPath,labelName.replace(labelSuffix,ip))
            if os.path.exists(n):
                segimagePath = n
        
        for ip in IMAGE_FORMAT:
            n = os.path.join(imgPath,labelName.replace(labelSuffix,ip))
            if os.path.exists(n):
                imagePath = n

        if imagePath == None or segimagePath == None :
           raise NameError("imagePath or segimagePath Error") 
        
        data = setDataInfo(
            labelPath= labelPath,
            imPath=imagePath,
            segImPath=segimagePath,
            labelType= labelType,
            clsInfo=clsInfo,
            colorInfo = colrInfo
        )
        unrealoutput.setData(data)      

    return unrealoutput

        
class setDataInfo:
    def __init__(self,labelPath,imPath,segImPath,labelType,clsInfo,colorInfo) -> None:
        self.label = labelPath
        self.ImPath = imPath
        self.labelType = labelType
        self.clsInfo = yaml_dict(clsInfo)
        self.segImPath = segImPath
        self.colorInfo = yaml_dict(colorInfo)

    def getLabelInfo(self):
        if self.labelType == LabelFormat.JSONForm:
            label = json_dict(self.label)
            label["fire"] = '200'
            label["black-smoke"] = "221"
            label["gray-smoke"] = "222"
            label["white-smoke"] = "223"
            return label 
        elif self.labelType == LabelFormat.TXTForm:
            label = TxtRead(self.label)
            return label
    def getcolorInfo(self): # mgen 전용 
        coloInfo_dict = {}
        info = self.getLabelInfo()
        for c,v in self.clsInfo.items():
            coloInfo_dict[v.lower()] = info[v.lower()] # color info - str, list 
        
        return coloInfo_dict
    
    def getclsInfo(self): # 한번에 하나의 class 객체를 만드는거라, key값 겹쳐도 상관없음 
        clsInfo_dcit = {}
        for c,v in self.clsInfo.items():
            clsInfo_dcit[v.lower()] = c

        return clsInfo_dcit 
    def getLabelName(self):
        return os.path.basename(self.label)
    def getYoloName(self):
        if self.labelType == LabelFormat.JSONForm:
            return os.path.basename(self.label).replace(".json",".txt")
        elif self.labelType == LabelFormat.TXTForm:
            return self.getLabelName
    
    def getLabelType(self):
        return self.labelType
    
    def getImg(self):
        return os.path.basename(self.ImPath)
    
    def getIm(self):
        return Image.open(self.ImPath)
    
    def getImSize(self):
        img = self.getIm()
        return img.size # w,h
    
    def getsegIm(self):
        return cv2.imread(self.segImPath)
    
    def getsegImSize(self):
        img = self.getsegIm()
        return img.shape #h,w,c
    
    def getsettingColorInfo(self):
        return self.colorInfo
    
class allUnreal:
    def __init__(self) -> None:
        self._output = []

    def setData(self,data):
        self._output.append(data)

    def removeAllData(self):
        self._output =[]

    def getDataset(self):
        return self._output