import os 
import shutil
from ..general import path_confirm
import cv2 

# origin 과 confrim image file list를 읽어와서 
# 없는 것들은 remove.txt 파일에 쓰고, 라인 확인 후 차이 맞으면 
# 해당 txt 파일에 있는 image파일 삭제 or move 

def compare_and_record(folder1, folder2, output_file):
    # 폴더 1과 폴더 2에서 파일 목록 가져오기
    files_folder1 = set(os.listdir(folder1))
    files_folder2 = set(os.listdir(folder2))
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

def moveFile(folder1,txtFile,move,name):
    with open(txtFile, 'r') as file:
        files_to_delete = file.read().splitlines()
    if move:
        move_save = path_confirm(f"./result/removeFile/{name}/")
        print(f"MoveDirectorys : {move_save}",)
    deleted_files_count = 0 
    for file_name in files_to_delete:
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

def chromaGenerating(chormapath):
    pass