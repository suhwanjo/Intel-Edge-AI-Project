# 비보호 좌회전 안전 보조 시스템 Server

## Hardware Setting
![Circuit](https://github.com/suhwanjo/Intel-Edge-AI-Project/assets/112834460/74d942c5-1912-4c0d-a894-16bf24ab9911)
위와 같이 회로도를 구성합니다.
## motion Configuration
본 프로젝트에서는 HTTP 기반의 Motion 소프트웨어를 사용해 실시간 영상 데이터를 전송합니다.
### Install motion
```shell
sudo apt-get install motion
```
### Change motion conf file
```shell
sudo nano /etc/motion/motion.conf
```
```bash
daemon on
webcontrol_localhost off
stream_localhost off
output_prictures off
ffmpeg_output_movies off
stream_maxrate 100
framerate 100
```
설정이 없다면 작성합니다.

```shell
sudo nano /etc/default/motion
```
```bash
start_motion daemon=yes
```
### Start motion
카메라 연결을 확인합니다.
```shell
ls /dev/video*
```
```bash
sudo service motion start
sudo motion -n
```
### Check straming web page
```shell
http://<ip>:8081
```
## Prerequisite
- python --version 3.10.12
```shell
cd ./Intel-Edge-AI-Project/ITS_YOUR_TURN_SERVER
python -m venv iyt_env
source iyt_env/bin/activate
(iyt_env) pip install -U pip
(iyt_env) pip install -r requirements.txt
(iyt_env) chmod 0700 /run/user/1000
```

## Steps to run
```shell
cd ./Intel-Edge-AI-Project/ITS_YOUR_TURN_SERVER
source iyt_env/bin/activate
(iyt_env) python3 qt.py
```
