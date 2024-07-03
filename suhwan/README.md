
# 0618 AI Hub를 통한 데이터 수집
## INNORIX EX Ubuntu 간단 사용 설명서

### 패키지 설치
[PDF 다운로드](https://www.aihub.or.kr/web-nas/aihub21/files/public/이노릭스%20다운로드/INNORIX-EX-Ubuntu%EC%9A%A9_%EA%B0%84%EB%8B%A8%20%EC%82%AC%EC%9A%A9%20%EC%84%A4%EB%AA%85%EC%84%9C_%EC%9B%B9%EA%B3%B5%EA%B0%9C%EC%9A%A9.pdf)

- `sudo dpkg -i ./INNORIX-EX-Agent-x64.deb` 명령어 실행 시 OpenSSL 버전 오류가 발생하면 다음 단계를 따르세요

### 패키지 다운로드

다른 미러 사이트를 사용하여 필요한 패키지를 다운로드합니다. 예를 들어

```bash
wget http://security.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb
```

### 다운로드한 패키지 설치

패키지를 다운로드한 후 `dpkg`를 사용하여 설치합니다

```bash
sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb
```

의존성 문제로 설치가 완료되지 않으면 다음 명령어를 실행하여 해결할 수 있습니다

```bash
sudo apt-get install -f
```

## Mozilla 오류 해결

새로운 오류 메시지가 Mozilla 관련 파일이 누락되었다고 할 경우, 다음 단계를 시도해 보세요

### 필수 패키지 설치

Mozilla 라이브러리와 관련된 패키지를 설치합니다

```bash
sudo apt-get update
sudo apt-get install libmozjs-60-0 libnss3
```

### 의존성 문제 해결

의존성 문제가 계속 발생하면 다음 명령어를 사용하여 모든 의존성 문제를 해결합니다

```bash
sudo apt-get install -f
```

### 다시 실행 시도

패키지를 설치한 후 다음 명령어를 사용하여 다시 실행해 보세요

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

INNORIX가 정상적으로 실행 중인지 확인하려면 다음 명령어를 사용합니다

```bash
netstat -antpl | grep innorix
```

## 브라우저 SSL 인증서

브라우저 SSL 인증서를 복사하려면 다음 명령어를 사용합니다

```bash
cp /opt/innorix-ex/ca.crt .
```

# 0619 데이터 추출 및 검수
- sign_extract.py
    - 압축 해제 후 ‘사각형’ ‘파란색’인 교통 표지판’만 추출하는 코드
    
## 파일 전송
```bash
scp -r <보낼경로> <사용자이름>@<IP>:<받을경로>
```
- 첫 전송 시 yes
- password 입력

# 0620 OTX 모델 학습
pot2
├── confidence_threshold
├── config.json
├── label_schema.json
├── openvino.bin
├── openvino.xml
├── ptq_performance.json

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

![performance_metrics](https://github.com/suhwanjo/Intel-Edge-AI-Project/assets/112834460/149c796d-6e35-4bc7-97a6-e50096e9f91c)

## 테스트 추론
inference.py

# 0623 신호등 신호 판단 알고리즘 개발
inference_sign_light.py
- 4개 segment 분리 후 평균 색상 계산

