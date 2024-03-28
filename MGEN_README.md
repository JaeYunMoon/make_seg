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
python mgen.py -ip C:\Users\sim2real\Desktop\personalProject\dataconfirm\make_seg\datasets\train\images -lp C:\Users\sim2real\Desktop\personalProject\dataconfirm\make_seg\datasets\json -seg C:\Users\sim2real\Desktop\personalProject\dataconfirm\make_seg\datasets\seg --confrim_image T
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

