
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

### 파일 이동 안할 시 
- 아래 옵션을 확인 후 상황에 argument 값을 수정 하면 된다.(Example 참고)


# 옵션 
## 파이썬 실행 시 Argument

| Argument &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description | Example | Default |
|:-------------:|:-----------:|:-----------:|:-----------:|
| `-h`,<br>`--help ` |	show help message | `python seg_make_to_txt.py -h` | |  
|  `-lt`,<br>`--LabelType` | 임시 argumentation 무시 해도 상관없음 | `python seg_make_to_txt.py -lt txt` |  |  
|  `-lp`,<br>`--LabelPath` | Directory that contains the Label data| `python seg_make_to_txt.py -lp ./labels` | ./labels |  
| `-ip`,<br>`--ImagePath` | Directory that contains the Image data | `python seg_make_to_txt.py -ip ./images` | ./images |  
| `-refer`,<br>`--colorCoordinate` | 언리얼에서 출력하는 segmentation 색상 별 라벨링된 파일  | `python seg_make_to_txt.py -refer ./refer/img_coor.json` | ./refer/img_coor.json|  
| `-cls_set`,<br>`--ClassYaml` | 딕셔너리 형태의 Yaml파일.<br> Label에 있는 라벨링 번호(key 값)와 라벨링에 해당하는 객체 명사 | `python seg_make_to_txt.py -cls_yaml ./refer/cls.yaml` | ./refer/cls.yaml |  
| `-colo_set`,<br>`--colorSetting` | 딕셔너리 형태의 Yaml파일.<br> 라벨마다 다른 색상 값을 부여하는 설정 값| `python seg_make_to_txt.py -cs ./refer/color.yaml` | ./refer/color.yaml |
| `-b`,<br>`--background` | 라벨 표시 할 때 테두리 내부 색상 입력 옵셥 True,False | `python seg_make_to_txt.py -b True` | `True` | |  
| `-lw`,<br>`--LineWidth` | 라벨 표시 할 때 테두리 두께 0.0~0.9 사이의 값 |  `python seg_make_to_txt.py -lw 0.5` | `0.3` |  
| `-sr`,<br>`--SaveRoot` | 추가 예정 | `python seg_make_to_txt.py -sr /home/my_results/` | `results/` |  
| `-cp`,<br>`--Company` | 회사마다 특수 케이스 해결하기 위한 옵션(구현 예정) | `python seg_make_to_txt.py -company True` |`False`|  

#### 파일 이동 시 Default값으로 설정했기 때문에 바로 실행 하면 된다. 
#### 라벨 이미지 표시 옵션은 색상은 refer/color.yaml 변경, 선두께 -lw 변경, -b 백그라운드 색깔 생성 
- 백그라운 색상은 선(테두리) 색상과 동일  