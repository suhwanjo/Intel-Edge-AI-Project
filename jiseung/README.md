## 6월 19일~6월 21일
---
* 비보호 좌회전 표지판 + 신호등 Annotation Rule

* data_annotation site 
    * ROBOFLOW   

* dataset_URL : https://universe.roboflow.com/intelaiprojectcar/intel_ai_project_car

* OTX 모델 학습 관련 사이트 :   https://openvinotoolkit.github.io/training_extensions/1.5.0/guide/tutorials/base/index.html
    * dataset 수정 버전 사진
	![Screenshot from 2024-07-03 10-21-30](https://github.com/suhwanjo/Intel-Edge-AI-Project/assets/163945374/b5a500fe-6998-4477-87a5-339937b5d620)

## 6월 23일
---
* ai의 신호등 인식 향상을 위해 gamma보정 활용
  :inference.py
  
  
## 6월 24일
---
* 메모리 용량 부분 최적화 코드
    :model_integration_fixmemory.py

| 모델 이름               | mAP   | time elapsed | epoch | f-measure | batch_size | learning_rate |
|-------------------------|-------|--------------|-------|-----------|------------|---------------|
| YOLOV8                  | 0.929 | -            | 120   | -         | -1         | -             |
| YOLOX-TINY              | 0.936 | 0:51:15      | 32    | 0.928     | 8          | 0.0002        |
| MobileNewV2-ATSS        | 0.920 | 0:57:30      | 24    | 0.900     | 8          | 0.004         |
| YOLOx-TINY(다른 에폭)   | 0.936 | 1:19:55      | 50    | 0.916     | 8          | 0.0002        |
| **Data_set 변경**       |**mAP**   | **time elapsed** | **epoch** | **f-measure** | **batch_size** | **learning_rate** |
| YOLOV8                  | 0.967 | -            | -     | -         | -1         | -             |
| YOLOX-TINY              | 0.948 | 4:10:19      | 11    | 0.924     | 8          | 0.0002        |
| SSD                     | 0.926 | 1:57:44      | 63    | 0.908     | 8          | 0.01          |

## 6월 25일
---
- 시스템 구조 변경
    
    ### 1. 시스템 성능 개선 → 라즈베리파이 추론 포기
    
    - 라즈베리파이(스트리밍 + 하드웨어) ↔ 데스크탑(추론) 통신으로 변경
    
    ### 2. 라즈베리파이
    - UI 개발 → PyQT
    - 하드웨어 → 스피커, 버튼
    

## 6/26~28 
---
* UI 개발, 라즈베리파이, 발표 자료 제작
### UI 개발 및 수정

- 좌회전 깜빡이 켰을 때만 데이터 수신
- 완성 코드
    클라이언트
        -main.py
        -traffic_sign_detection.py
        -vehicle_detection.py
        -vedio_processor.py
    서버
        -final_UI_short.py
<깃허브에서 확인 가능>

##6/29~7/1
## 발표자료 수정 
![Screenshot from 2024-07-03 13-42-06](https://github.com/suhwanjo/Intel-Edge-AI-Project/assets/163945374/dcd7b5a2-9f71-4be9-b392-4c14a5e5cc69)
## 기능적 보안 및 시연 영상 촬영

![Screenshot from 2024-07-03 13-43-09](https://github.com/suhwanjo/Intel-Edge-AI-Project/assets/163945374/305d3a94-ba75-4060-bdc8-19b60260ea8e)
