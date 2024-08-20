# 이츠 유얼 턴
비보호 좌회전 안전 보조 시스템, It's your turn!

프로젝트 정리 Notion 링크 : https://www.notion.so/bd0689ee7531443caedd767db4489506?pvs=4   


![image](https://github.com/user-attachments/assets/264d1ccb-edd8-4bf5-bda4-f581c762fa05)


## Contents
- [Outline](#Outline)
- [Team](#Team)
- [Stacks](#Stacks)
- [Motivation](#Motivation)
- [Project Schedule](#Project-Schedule)
- [Prerequisite](#Prerequisite)
- [High Level Design](#High-Level-Design)
- [Low Level Design](#Low-Level-Design)
- [Used AI Model](#Used-AI-Model)
- [Output](#Output)

## Outline
프로젝트 주제: AI를 활용한 서비스 제작

프로젝트 수행자: 인텔 엣지 AI SW 개발자 아카데미 4기 / 팀 이츠유얼턴 (김승민, 박민혁, 유지승, 조수환)

프로젝트 수행기간: 24/06/20 ~ 24/07/02

* 라즈베리파이와 태블릿을 사용하여 비보호 좌회전 시 교통 안전을 보조하는 디지털 계기판 디스플레이 시스템의 프로토타입을 구현합니다.
* 이 시스템은 교통 표지판, 신호등을 인식하고, 반대 차선의 차량을 감지하여 안전한 좌회전을 돕습니다.

## Team

* Members
  | Name | Role |
  |----|----|
  | 김승민 | Project lead, Hardware Setup  |
  | 박민혁 | UI design, AI modeling    |
  | 유지승 | AI modeling, Project Manager   |
  | 조수환 | AI modeling, System integration |
  
* Project Github : https://github.com/suhwanjo/Intel-Eged-AI-Project.git
* 발표자료 : https://github.com/kccistc/intel-04/tree/main/doc/project/team_5

## Stacks
### Front-End

<img src="https://img.shields.io/badge/QT-41CD52?style=for-the-badge&logo=QT&logoColor=white">

### Back-End

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"><img src="https://img.shields.io/badge/OpenVINO-412991?style=for-the-badge&logo=intel&logoColor=white"><img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=OpenCV&logoColor=white"><img src="https://img.shields.io/badge/Numpy-013243?style=for-the-badge&logo=Numpy&logoColor=white">

<img src="https://img.shields.io/badge/Threading-013243?style=for-the-badge&logo=Threading&logoColor=white"><img src="https://img.shields.io/badge/Socket-013243?style=for-the-badge&logo=Socket&logoColor=white">

### Hardware

Raspberry Pi 4(4GB), Web Cam, Buzzer, Raspberry Pi Touch Display(7”)


## Motivation
### 문제 정의
#### 비보호 좌회전 시 발생한 사고
* 통계
    * 교통사고 통계에 따르면 비보호 구역 내 도로에서 발생하는 교통사고 발생률이 일반 도로보다 30% 높은 수준입니다.
* 문제 인식
    * 비보호 좌회전은 종종 운전자에게 혼란을 주고 교통 사고의 주요 원인 중 하나로 작용합니다. 특히 교차로에서의 판단 착오로 인해 사고가 발생할 가능성이 큽니다.

#### 프로젝트 필요성
* 운전자 교육 및 인식 개선
    * 많은 운전자들이 교통법규를 제대로 알지 못하거나 오해하여 발생하는 사고가 많습니다. 이 프로젝트는 실시간 도로 정보와 신호를 제공함으로써 이러한 문제를 해결하고자 합니다.
* 안전한 운전 환경 조성
    * 운전자들에게 교차로에서의 비보호 좌회전 시 안전한 판단을 도울 수 있는 시스템을 제공함으로써, 교통 상황을 명확하게 인지하고 안전한 운전 환경을 조성할 수 있습니다.
* 교통 사고 예방
    * 실시간 도로 정보와 신호를 제공하여 운전자의 판단을 돕고, 이를 통해 교통 사고를 예방할 수 있습니다. 이는 교통 체계의 효율성 향상에도 기여할 것입니다.

#### 기대 효과
* 안전한 교차로 주행
    * 본 시스템이 구현되면, 교차로에서의 비보호 좌회전 시 안전한 판단을 돕는 기능을 제공함으로써 교통 사고를 크게 줄일 수 있을 것입니다.
* 교통사고 감소
    * 교통사고 통계에 따르면 비보호 구역 내 도로에서 발생하는 교통사고 발생률이 일반 도로보다 30% 높은 수준입니다. 이 시스템을 통해 비보호 구역에서의 사고를 효과적으로 감소시킬 수 있습니다.
* 교통 흐름 개선
    * 실시간으로 도로 상태와 신호 정보를 제공함으로써 교통 흐름을 더 원활하게 하고, 운전자의 예측 가능성을 높여 교차로에서의 교통 혼잡을 줄일 수 있습니다.
* 운전자 신뢰도 향상
    * 운전자들이 교통 상황을 명확히 인지하고 안전하게 주행할 수 있도록 도와줌으로써, 전체 교통 시스템에 대한 신뢰도를 향상시킬 수 있습니다.

## Project Schedule
![plan](https://github.com/suhwanjo/Intel-Eged-AI-Project/assets/112834460/6662b3db-6ef7-4363-9631-36c73bb08e2f)

## Prerequisite
### Clone Code
```shell
https://github.com/suhwanjo/Intel-Edge-AI-Project.git
```
- [Steps to run - Server](https://github.com/suhwanjo/Intel-Edge-AI-Project/blob/main/ITS_YOUR_TURN_SERVER/README.md)
- [Steps to run - Client](https://github.com/suhwanjo/Intel-Edge-AI-Project/blob/main/ITS_YOUR_TURN_CLIENT/README.md)

## High Level Design

### System Architecture
![Untitled (2)](https://github.com/suhwanjo/Intel-Eged-AI-Project/assets/112834460/5fe7b7f4-d99a-4adf-b7b0-26b116c604b4)

### Flow Chart
![제목 없는 다이어그램 drawio (3)](https://github.com/suhwanjo/Intel-Edge-AI-Project/assets/112834460/2779a6e6-48e3-48e0-86a7-ea3c93a4362d)

## Low Level Design
### 기능 명세서

#### 각 기능의 세부 요구사항

1. **좌회전 인식**
    - 방향 지시등 대체 스위치를 통해 좌회전 시작을 인지
    - 방향 지시등 신호가 입력되면 시스템 활성화

2. **교통 표지판 및 신호 인식**
    - 비보호 좌회전 표지판 인식
    - 신호등 인식 및 신호 분석

3. **반대 차선 차량 인식**
    - 반대 차선 차량 감지.
    - 차량의 거리 측정 및 거리 추정

4. **안전 판단**
    - 교통 표지판 정보 및 반대 차선 차량 정보를 종합하여 안전 여부 판단
    - 판단 결과를 실시간으로 HUD에 표시

5. **HUD 디스플레이**
    - 태블릿을 통해 운전자가 쉽게 볼 수 있는 HUD 화면 구현
    - 안전 여부 및 관련 정보를 시각적으로 표시

### 기능별 우선순위

1. 좌회전 인식
2. 교통 표지판 및 신호 인식
3. 반대 차선 차량 인식
4. 안전 판단
5. HUD 디스플레이

### Sequence Diagram
![Untitled diagram-2024-06-27-081944](https://github.com/suhwanjo/Intel-Eged-AI-Project/assets/112834460/60a3c231-437b-4e59-98e1-0b75d344db51)

### Class Diagram
![image](https://github.com/suhwanjo/Intel-Edge-AI-Project/assets/112834460/ebba343d-e2e9-40f0-9908-7016d32c10e0)

## Used AI Model
### 신호등&비보호 좌회전 표지판 감지
1. backbone
    - Custom_Object_Detection_YOLOX (otx 제공 pretrained model)

2. data
    - AI hub 데이터 : 1,703장
    - 수집 방법 : AI hub 데이터 - 라벨링 데이터로 유사 표지판 추출 후 직접 검수
3. Model 전이학습 과정
    - Roboflow로 COCO 데이터셋 구축
    - otx build
    - train
    - export half-precision
    - optimize pot 
    - deploy
4. Model별 Training 결과
    * 1차
      | 모델 이름 | mAP | time elapsed | epoch | f-measure | batch_size | learning_rate |
      | --- | --- | --- | --- | --- | --- | --- |
      | YOLOV8 | 0.929 | - | 120 | - | -1 | - |
      | YOLOX-TINY | 0.936 | 0:51:15 | 32 | 0.928 | 8 | 0.0002 |
      | MobileNewV2-ATSS | 0.920 | 0:57:30 | 24 | 0.900 | 8 | 0.004 |
      | YOLOx-TINY(다른 에폭) | 0.936 | 1:19:55 | 50 | 0.916 | 8 | 0.0002 |
    * 2차
      | 모델 이름 | mAP | time elapsed | epoch | f-measure | batch_size | learning_rate |
      | --- | --- | --- | --- | --- | --- | --- |
      | YOLOV8 | 0.967 | - | - | - | -1 | - |
      | YOLOX-TINY | 0.948 | 4:10:19 | 11 | 0.924 | 8 | 0.0002 |
      | SSD | 0.926 | 1:57:44 | 63 | 0.908 | 8 | 0.01 |
      
### 차량 감지
- backbone
    - vehicle-detection-0200
### 거리 예측
- backbone
    - midasnet(monodepth)
 
## Output
### 비보호 좌회전 및 신호 인식 화면
적색 신호 시

![image](https://github.com/suhwanjo/Intel-Edge-AI-Project/assets/112834460/42b4ed33-851d-402b-ab08-1b3320392d97)

청색 신호 시

![image](https://github.com/suhwanjo/Intel-Edge-AI-Project/assets/112834460/81155ca6-d217-403e-8895-d6b85330524f)


### 차량 및 거리 예측 화면
거리 100 이상

![image](https://github.com/suhwanjo/Intel-Edge-AI-Project/assets/112834460/b8416e31-650c-4e64-9f95-c234b4ec1ce3)

거리 100 미만

![image](https://github.com/suhwanjo/Intel-Edge-AI-Project/assets/112834460/9a5a212b-4fa0-4738-b838-e40d7a00a49e)

### GUI
![image](https://github.com/suhwanjo/Intel-Edge-AI-Project/assets/112834460/8c361c69-2cb9-4b37-b2f8-ba2b9f404148)
