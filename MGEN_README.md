# 진행 순서 

## 코드 실행 전 가상환경 설치 
```
conda create -n mgen pytho=3.8 
conda activate mgen 

# 필요시 
# python.exe -m pip install --upgrade pip

# git clone
git clone https://github.com/JaeYunMoon/make_seg.git

```
## 예시 
### mgen_finish.py 

```
python mgen_finish.py --chroma True -cimg D:\add_storage\datasets\result\ConfrimImg -oimg D:\add_storage\datasets\train\images -l D:\add_storage\datasets\result\YoloForm -seg D:\add_storage\datasets\result\MgenFormSegimg -fm True

```
```
# 위 파이썬 파일 설명 

# -fm : 삭제 해야할 파일(conform image에서 지운 이미지) 삭제 하지 않고, 다른 폴더로 이동 (하드 용량 괜찮다면 True 지향)
# --chroma : chroma 생성 시 True, 아니면 False (이전 납품 데이터 경우)
# -cimg : ConfrimImg Directory 경로 
# -oimg : 원본(unreal)이미지 - 삭제하기 위해 / 크로마 True인 경우 크로마 생성 하기 위해 
# -l : yolo 형식의 라벨링 txt파일 모여있는 Directory 경로 - 삭제하기 위해 
# -seg : Mgen형식의 segmentation Directory 경로 

---
# 추가 옵션 
# -sr : 저장 경로 (Default = "./result/")
# -refer : segmentation 색상 좌표 json 경로 (Default = "./refer/img_coor.json)
```

### mgen.py 

```
python mgen.py -lp D:\add_storage\datasets\json -ip D:\add_storage\datasets\train\images  -seg D:\add_storage\datasets\seg --confirm_image True 
```
```
# 위 파이썬 파일 설명 
# -lp : (unreal output) json Directory 경로 
# -ip : (unreal output) image Directoy 경로 
# -seg : (unreal output) segmentation Directory 경로 
# --confirm_image : 데이터 확인 하기 위한 이미지 생성 Bool 
---
# 추가 옵션 
# -sr : 저장 경로 (Default = "./result/")
# -refer : segmentation 색상 좌표 json 경로 (Default = "./refer/img_coor.json)
# -colo_set : 라벨(Class)별 데이터 확인 시 색상 정한 yaml파일 경로 
# -b : 라벨 확인 시 polyLine 내부 색상 (default = False, 배경 색 없음)
# -lw : 라벨 확인시 polyLine 두께

```

## git clone 후 
- 기존과 동일하게 데이터가 있는 Directory 에 파일을 옮겨서 실행 해도 된다. 
### 파일 이동 시 
- seg_make_to_txt.py (변경 가능 성 있음) 
- /utils (Directory)
- /refer (Directory)

위 파일들을 이동 시키면 된다. 

# 옵션 

- 아래 코드 줄 경로만 변경해서 실행, confrim image까지 한번에 진행 DataConfrim.py 따로 실행 안해도 됨.

```
python mgen.py -ip C:\Users\sim2real\Desktop\personalProject\dataconfirm\make_seg\datasets\train\images -lp C:\Users\sim2real\Desktop\personalProject\dataconfirm\make_seg\datasets\json -seg C:\Users\sim2real\Desktop\personalProject\dataconfirm\make_seg\datasets\seg --confirm_image T
```

## 파이썬 실행 시 Argument

| Argument &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description | Example | Default |
|:-------------:|:-----------:|:-----------:|:-----------:|
| `-h`,<br>`--help ` |	show help message | `python mgen.py -h` | |  
|  `-lt`,<br>`--LabelType` | 임시 argumentation 무시 해도 상관없음 | `python mgen.py -lt txt` |  |  
|  `-lp`,<br>`--LabelPath` | Directory that contains the Label data| `python mgen.py -lp ./labels` | ./labels |  
| `-ip`,<br>`--ImagePath` | Directory that contains the Image data | `python mgen.py -ip ./images` | ./images |  
| `-refer`,<br>`--colorCoordinate` | 언리얼에서 출력하는 segmentation 색상 별 라벨링된 파일  | `python mgen.py -refer ./refer/img_coor.json` | ./refer/img_coor.json|  
| `-cls_set`,<br>`--ClassYaml` | 딕셔너리 형태의 Yaml파일.<br> Label에 있는 라벨링 번호(key 값)와 라벨링에 해당하는 객체 명사 | `python mgen.py -cls_yaml ./refer/cls.yaml` | ./refer/cls.yaml |  
| `-colo_set`,<br>`--colorSetting` | 딕셔너리 형태의 Yaml파일.<br> 라벨마다 다른 색상 값을 부여하는 설정 값| `python mgen.py -cs ./refer/color.yaml` | ./refer/color.yaml |
| `-sr`,<br>`--SaveRoot` | 추가 예정 | `python mgen.py -sr /home/my_results/` | `results/` |  
| `-seg`,<br>`--SegImPath` | Directory that contains the Segmentation Image data | `python mgen.py -seg  ./seg` |`./seg`| 
| `-b`,<br>`--background` | 라벨 표시 할 때 테두리 내부 색상 입력 옵셥 True,False | `python mgen.py -b True` | `True` | |  
| `-lw`,<br>`--LineWidth` | 라벨 표시 할 때 테두리 두께 0.0~0.9 사이의 값 |  `python mgen.py -lw 0.5` | `0.3` |  
| `--confirm_image` | yolo 라벨링 확인하는 옵션  | `python mgen.py --confirm_image T` | `` |  


