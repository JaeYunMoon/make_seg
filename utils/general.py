import os 
from typing import List 
import argparse
from enum import Enum
import json

try:
    import yaml 
    from easydict import EasyDict as edict
except:
    os.system("pip install PyYAML")
    os.system("pip install easydict")
    import yaml 
    from easydict import EasyDict as edict

def check_dir_list(directorys:str,nameArg:str) -> List:
    """
    Input:
        directorys : Path (str)
        nameArg : parse_option name (str) 
    Fuction:
        directorys 경로 받아서 경로가 잘못되어 있는지 확인 후
        directorys 안에 txt파일이 있는지 확인 
        nameArg은 로그를 위한 값 잘못 되었을 때 parse_opt중에 어떤게 잘 못 되어 있는지 확인하는 용도 
    
    output:
        File list(list) : Directorys 안에 있는 파일  
        
    """
    dirs = directorys.replace("\\",os.sep)
    assert os.path.isdir(dirs),f"argument {nameArg} : Directory does not exist{directorys}"
    files_list = os.listdir(dirs)
    f = [os.path.join(directorys,file) for file in files_list]
    assert not len(f) == 0,f"argument {nameArg} : .txt files does not exist in Directory{directorys}"
    
    return f

def path_confirm(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return os.path.abspath(path)

def TxtRead(path):
    with open(path,"r") as f:
        objs = f.readlines()
        yield objs

def changeAbsPath(path,name):
    if os.path.exists(path):
        return os.path.abspath(path)
    else:
        raise FileExistsError(f"{name} Error,Please Check {name}")
    
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
    
def checkLabelSuffix(argSuffix):
    if str(argSuffix) == ".txt":
        return LabelFormat.TXTForm
    elif str(argSuffix) == ".json":
        return LabelFormat.JSONForm
    else:
        raise TypeError(f"Label Type : txt or json Not {argSuffix}")
    
def json_dict(jpth):
    with open(jpth,"r",encoding="cp949") as f:
        js_file = edict(json.load(f))
    return js_file

def yaml_dict(ypth):
    with open(ypth) as f:
        data = yaml.load(f,Loader=yaml.FullLoader)
    return data 

class LabelFormat(Enum):
    TXTForm = 1
    JSONForm =2 

