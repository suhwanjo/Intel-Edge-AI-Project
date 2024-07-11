# 비보호 좌회전 안전 보조 시스템 Client

## Prerequisite
- python --version 3.10.12
```shell
cd ./Intel-Edge-AI-Project/ITS_YOUR_TURN_CLIENT
python -m venv iyt_env
source iyt_env/bin/activate
(iyt_env) pip install -U pip
(iyt_env) pip install -r requirements.txt
```
main.py의 video_path를 Server 장치의 실시간 영상을 스트리밍하는 HTTP 주소로 수정합니다.

## Steps to run
```shell
cd ./Intel-Edge-AI-Project/ITS_YOUR_TURN_CLIENT
source iyt_env/bin/activate
(iyt_env) python3 main.py
```
Server 장치의 IP를 입력합니다.
