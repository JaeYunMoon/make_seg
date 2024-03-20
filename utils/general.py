import os 
from typing import List 

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
    f = [os.path.join(directorys,file) for file in files_list if file.endswith(".txt")]
    assert not len(f) == 0,f"argument {nameArg} : .txt files does not exist in Directory{directorys}"
    
    return f

def path_confirm(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return os.path.abspath(path)

def TxtRead(path):
    with open(path,"r") as f:
        objs = f.readlines()
        return objs