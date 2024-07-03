import socket
import json

HOST = '127.0.0.1'  # 서버 IP 주소(로컬)
PORT = 5001  # 서버 포트

# 전송할 JSON 데이터
data = {"left_sign_detected": True,
        "current_green_light": True,
        "depth_value": 200
        }

# TCP 소켓 생성
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # 서버에 연결
    s.sendall(json.dumps(data).encode())  # JSON 형식의 데이터를 전송
