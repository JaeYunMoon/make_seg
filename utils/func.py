import os 
import re
from .general import path_confirm
from pathlib import Path 
import numpy as np 
from tqdm import tqdm


try:
    import matplotlib.pyplot as plt 
    from matplotlib.patches import Polygon
    from matplotlib.collections import PatchCollection

except:
    os.system("pip install matplotlib")

    import matplotlib.pyplot as plt    
    from matplotlib.patches import Polygon
    from matplotlib.collections import PatchCollection

def drawNewSeg(js,new_seg_folder):
    pass 

def ConfirmImage(objs,backgroundColor,LineWidth,saveRoot):
    save_root = saveRoot
    for obj in tqdm(objs):
    
        plt.imshow(obj.getIm());plt.axis("off");ax=plt.gca()
        polygons = []
        color = [] 
        title = ""
        # title = Path(obj.labelPath).name
        # print(obj.getSettingColor)
        w,h = obj.getImageSize()
        for k,v in obj.getLabelInfo().items():
            t = f"({obj.getclsDict()[k]} : {len(v)}) "
            title +=t
            c = obj.getSettingColor()[k]
            # c = (np.random.random((1, 3))*0.6+0.4).tolist()[0]

            for coor in v:
                poly = np.array(coor,dtype=np.float32).reshape((int(len(coor)/2),2))
                poly[:,:1] = poly[:,:1]*w
                poly[:,1:] = poly[:,1:]*h 
                polygons.append(Polygon(poly))
                color.append(c)
                if not backgroundColor:
                    p = PatchCollection(polygons, facecolor=color, linewidths=0, alpha=0.4)
                    ax.add_collection(p)
                else:
                    pass 
                p = PatchCollection(polygons, facecolor='none', edgecolors=color, linewidths=LineWidth) 
                ax.add_collection(p)
        

        plt.title(str(title))
        # print(str(obj.getImTitle()))
        save = os.path.join(save_root,f"{str(obj.getImTitle())}")
        
        plt.savefig(save,bbox_inches='tight', pad_inches=0,dpi = 300)
        plt.clf()

    return save


