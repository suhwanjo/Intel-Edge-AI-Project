# 목차

1. [0618 AI Hub를 통한 데이터 수집](#0618-ai-hub를-통한-데이터-수집)
2. [0619 데이터 추출 및 검수](#0619-데이터-추출-및-검수)
3. [0620 OTX 모델 학습](#0620-otx-모델-학습)
4. [0623 신호등 신호 판단 알고리즘 개발](#0623-신호등-신호-판단-알고리즘-개발)
5. [0624 모델 통합 및 최적화](#0624-모델-통합-및-최적화)
6. [0625 시스템 아키텍처 변경](#0625-시스템-아키텍처-변경)
7. [0626 코드 클래스화&통신 추가](#0626-코드-클래스화통신-추가)
8. [0627-0628 UI 개발](#0627-0628-UI-개발)

   
---

# 0618 AI Hub를 통한 데이터 수집
## INNORIX EX Ubuntu 간단 사용 설명서

### 패키지 설치
[PDF 다운로드](https://www.aihub.or.kr/web-nas/aihub21/files/public/이노릭스%20다운로드/INNORIX-EX-Ubuntu%EC%9A%A9_%EA%B0%84%EB%8B%A8%20%EC%82%AC%EC%9A%A9%20%EC%84%A4%EB%AA%85%EC%84%9C_%EC%9B%B9%EA%B3%B5%EA%B0%9C%EC%9A%A9.pdf)

- `sudo dpkg -i ./INNORIX-EX-Agent-x64.deb` 명령어 실행 시 OpenSSL 버전 오류가 발생하면 다음 단계를 따르세요.

### 패키지 다운로드

다른 미러 사이트를 사용하여 필요한 패키지를 다운로드합니다. 예를 들어

```bash
wget http://security.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb
```

### 다운로드한 패키지 설치

패키지를 다운로드한 후 `dpkg`를 사용하여 설치합니다.

```bash
sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb
```

의존성 문제로 설치가 완료되지 않으면 다음 명령어를 실행하여 해결할 수 있습니다.

```bash
sudo apt-get install -f
```

## Mozilla 오류 해결

새로운 오류 메시지가 Mozilla 관련 파일이 누락되었다고 할 경우, 다음 단계를 시도해 보세요.

### 필수 패키지 설치

Mozilla 라이브러리와 관련된 패키지를 설치합니다.

```bash
sudo apt-get update
sudo apt-get install libmozjs-60-0 libnss3
```

### 의존성 문제 해결

의존성 문제가 계속 발생하면 다음 명령어를 사용하여 모든 의존성 문제를 해결합니다.

```bash
sudo apt-get install -f
```

### 다시 실행 시도

패키지를 설치한 후 다음 명령어를 사용하여 다시 실행해 보세요.

```bash
/opt/innorix-ex/innorixes start
```

### 로그 확인

추가적인 문제가 발생하면 로그 파일을 확인합니다. 로그 파일은 `/var/log` 디렉토리 또는 프로그램의 특정 디렉토리에 있을 수 있습니다. 예를 들어

```bash
cat /var/log/innorixes.log
```

문제가 계속 발생하면 구체적인 오류 메시지를 알려주시면 더 구체적인 도움을 드릴 수 있습니다.

## 확인

INNORIX가 정상적으로 실행 중인지 확인하려면 다음 명령어를 사용합니다.

```bash
netstat -antpl | grep innorix
```

## 브라우저 SSL 인증서

브라우저 SSL 인증서를 복사하려면 다음 명령어를 사용합니다.

```bash
cp /opt/innorix-ex/ca.crt .
```
---

# 0619 데이터 추출 및 검수
*sign_extract.py*
- 압축 해제 후 ‘사각형’ ‘파란색’인 교통 표지판’만 추출하는 코드입니다.
    
## 파일 전송
```bash
scp -r <보낼경로> <사용자이름>@<IP>:<받을경로>
```
- 첫 전송 시 yes
- password 입력
---

# 0620 OTX 모델 학습
```shell
pot2
├── confidence_threshold
├── config.json
├── label_schema.json
├── openvino.bin
├── openvino.xml
├── ptq_performance.json
```

## 모델

**YOLOX-TINY**

## 하이퍼파라미터

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
## 성능 확인

### 훈련 모드

- Epoch: 32
- Iteration: 491
- Learning Rate: 0.0
- Memory: 2545 MB
- Current Iterations: 15711
- Data Time: 0.03225 sec
- Loss (Classification): 0.51633
- Loss (Bounding Box): 1.80033
- Loss (Objectness): 0.54884
- Total Loss: 2.8655
- Gradient Norm: 25.04388
- Time per Iteration: 0.28366 sec

### 검증 모드

- Epoch: 32
- Iteration: 47
- Learning Rate: 0.0
- AP50: 0.937
- mAP: 0.93689
- Current Iterations: 15712

### 추가 성능 지표

- F-measure: 0.9288256227758006

### 총 경과 시간

- Time Elapsed: 0:51:15.941332

### 최적화

- Optimize with OpenVINO POT
- Precision Compress to FP16

## 테스트 추론
*inference.py*

![performance_metrics](https://github.com/suhwanjo/Intel-Edge-AI-Project/assets/112834460/149c796d-6e35-4bc7-97a6-e50096e9f91c)

---

# 0623 신호등 신호 판단 알고리즘 개발
*inference_sign_light.py*
- 신호등 객체를 4개의 segment로 분리한 후 평균 밝기를 계산합니다.
---

# 0624 모델 통합 및 최적화
## 데스크탑에서의 테스트
### 블랙박스 영상(60s)
*model_integration.py*
- 모델을 통합합니다.(88s)

*test.py.py*
- 멀티 스레딩을 추가합니다.(16s)

*test3.py*
- 하나의 스레드를 추가하고 최적화합니다.(7s)
	1. 단순화된 구조
	    - 함수 기반 설계로 코드가 간결하고 읽기 쉬움.
	2. 모델 로딩 및 전처리 분리
	    - 재사용 가능한 독립 함수(load_model, preprocess_frame) 사용.
	3. 명확한 프로세스 흐름
	    - 명시적 스레드 관리로 병렬 처리 효율성 향상.
	4. 간소화된 후처리 로직
	    - 간결한 후처리 함수로 불필요한 복잡성 제거.
	5. 효율적인 프레임 처리
	    - process_interval을 사용하여 불필요한 연산 감소.
	6. 최소화된 의존성
	    - 간소한 클래스 구조로 메모리 사용량 및 코드 복잡성 감소.
	7. 직관적인 데이터 흐름
	    - 명확한 데이터 전달로 디버깅 및 유지 보수 용이.
---

# 0625 시스템 아키텍처 변경
## 온디바이스 -> 소켓 통신(서버-클라이언트)
소켓 통신 테스트

*server.py*
- 서버로, 라즈베리파이에서 실행됩니다.

*client.py*
- 클라이언트로, 데스크탑이나 노트북에서 실행됩니다.
---

# 0626 코드 클래스화&통신 추가
*main.py*

*traffic_sign_detection.py*
- 신호등 및 비보호 좌회전 표지판 인식 및 처리 스레드입니다.

*vehicle_detection.py*
- 차량 인식 및 거리 예측 스레드입니다.

*video_processor.py*
- 실시간 영상의 프레임 처리 스레드입니다.
---

# 0627-0628 UI 개발
*qt.py*
- PyQT를 사용한 GUI입니다.

