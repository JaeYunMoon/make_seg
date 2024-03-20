import os 
import re
from .general import path_confirm
from pathlib import Path 
import numpy as np 


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

def ConfirmImage(obj,backgroundColor):
    save_root = path_confirm("./result")
    plt.imshow(obj.getIm());plt.axis("off");ax=plt.gca()
    polygons = []
    color = [] 
    title = Path(obj.labelPath).name
    w,h = obj.getImageSize()
    for ob in obj.getLabelInfo():
        ls = [d for d in ob.strip().split(" ")]
        coo = [re.sub("[^0-9.]","",x) for x in ls[1:]]
        coor = [float(x) for x in coo]
        c = (np.random.random((1, 3))*0.6+0.4).tolist()[0]

        poly = np.array(coor,dtype=np.float32).reshape((int(len(coor)/2),2))
        poly[:,:1] = poly[:,:1]*w
        poly[:,1:] = poly[:,1:]*h 
        polygons.append(Polygon(poly))
        color.append(c)
    if backgroundColor:
        p = PatchCollection(polygons, facecolor=color, linewidths=0, alpha=0.4)
        ax.add_collection(p)
    else:
        pass 
    p = PatchCollection(polygons, facecolor='none', edgecolors=color, linewidths=0.3) 
    ax.add_collection(p)
    

    plt.title(str(title))
    save = os.path.join(save_root,f"{str(title)}_seg.png")
    
    plt.savefig(save,bbox_inches='tight', pad_inches=0,dpi = 300)
    plt.clf()
    return save


