!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="XK1dF6S6SaLL1TfHLyWQ")
project = rf.workspace("intelaiprojectcar").project("intel_ai_project_car")
version = project.version(2)
dataset = version.download("yolov8")

!cat Intel_AI_Project_Car-2/data.yaml

import yaml
# yaml 파일 생성

# train, test, val 경로 지정
data = {'train' : '/home/ubuntu/ann/Intel_AI_Project_Car-2/train/images',
        'val' : '/home/ubuntu/ann/Intel_AI_Project_Car-2/valid/images',
        'test' : '/home/ubuntu/ann/Intel_AI_Project_Car-2/test/images',
        'names' : ['left_traffic_sign','traffic_light'],
        'nc' : 2}

# 학습 데이터 정보를 dump
with open('/home/ubuntu/ann/Intel_AI_Project_Car-2/SIGNLIGHT.yaml', 'w') as f:
  yaml.dump(data,f)

# yaml 파일로 저장
with open('/home/ubuntu/ann/Intel_AI_Project_Car-2/SIGNLIGHT.yaml', 'r') as f:
  scooter_yaml = yaml.safe_load(f)


from ultralytics import YOLO

# 사전 학습된 YOLO모델
model = YOLO('yolov8n.pt')

print(type(model.names), len(model.names))

print(model.names)

# yaml 파일을 통해 학습
model.train(data='/home/ubuntu/ann/Intel_AI_Project_Car-2/SIGNLIGHT.yaml', epochs=150, patience=10, imgsz=640)