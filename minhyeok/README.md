# 목차
- [06/19](#0619)
  - [어노테이션 및 라벨링](#어노테이션-및-라벨링)
- [06/20](#0620)
  - [데이터 수정 및 추가](#데이터-수정-및-추가)
  - [모델 학습](#모델-학습)
  - [학습 결과](#학습-결과)


# 06/19
## 어노테이션 및 라벨링
약 7,000장의 이미지 중 약 **700장**의 이미지를 선별 후 어노테이션 및 라벨링 작업 수행

<img src="https://github.com/suhwanjo/Intel-Edge-AI-Project/assets/96771644/9966c968-bd13-4470-9571-9f9af81c8c4c" width="500" height="300">

# 06/20
## 데이터 수정 및 추가
약 4,000장의 이미지 중 약 **400장**의 이미지를 선별 후 어노테이션 및 라벨링 작업 수행  
1차 데이터 삭제 및 추가 -> 라벨링의 폭을 넓게 수정

<img src="https://github.com/suhwanjo/Intel-Edge-AI-Project/assets/96771644/440bf3d3-2b31-4b24-8d5d-a4ef37371ccc" width="500" height="300">

## 모델 학습
OTX의 YOLOX-TINY 모델로 학습

<img src="https://github.com/suhwanjo/Intel-Edge-AI-Project/assets/96771644/e9751dc8-d62a-440a-9f66-74058d65ae34" width="500" height="300">

## 학습 결과
### 모델
`YOLOX-TINY`

### 하이퍼 파라미터
```yaml
learning_parameters:
  batch_size:
    default_value: 8
    auto_hpo_state: POSSIBLE
  inference_batch_size:
    default_value: 8
  learning_rate:
    default_value: 0.0002
    auto_hpo_state: POSSIBLE
  learning_rate_warmup_iters:
    default_value: 3
  num_iters:
    default_value: 200

```

### 성능확인

#### 훈련 성능 (mode: train)
| 항목                | 값           |
| ------------------- | ------------ |
| Epoch               | 50           |
| Iteration           | 246          |
| Learning Rate       | 0.0          |
| Memory              | 4806         |
| Current Iterations  | 12299        |
| Data Time           | 0.00948      |
| Loss (Class)        | 0.50077      |
| Loss (BBox)         | 1.72361      |
| Loss (Object)       | 0.53585      |
| 총 Loss             | 2.76023      |
| Gradient Norm       | 20.67017     |
| Time                | 0.3692       |

#### 검증 성능 (mode: val)
| 항목                 | 값           |
| ------------------   | ------------ |
| Epoch                | 50           |
| Iteration            | 47           |
| Learning Rate        | 0.0          |
| AP50                 | 0.937        |
| mAP                  | 0.9367       |
| Current Iterations   | 12300        |

#### F-Measure(정밀도와 재현율의 조화 평균)
`f-measure: 0.9162516976007243`

#### 경과 시간
`time elapsed: '1:19:55.974833'`
