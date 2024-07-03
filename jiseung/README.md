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
