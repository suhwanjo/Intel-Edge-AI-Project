import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtNetwork import QTcpServer, QHostAddress
from PyQt5.QtGui import QPixmap
import json

class ServerWindow(QMainWindow):
    def __init__(self):
        ''' 객체 초기화 '''
        super().__init__()
        self.tcpServer = QTcpServer(self)
        self.tcpServer.newConnection.connect(self.new_connection)
        
        port = 5001  # 포트 번호 지정
        if not self.tcpServer.listen(QHostAddress.Any, port):
            print(f"Failed to start server on port {port}")
        
        # UI 구성
        self.initUI()

    def initUI(self):
        ''' UI 구성 '''
        self.centralWidget = QWidget()
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Waiting for data...", self)
        self.layout.addWidget(self.label)
        
        self.leftSignLabel = QLabel("Left Sign: ", self)
        self.layout.addWidget(self.leftSignLabel)
        
        self.greenLightLabel = QLabel("Green Light: ", self)
        self.layout.addWidget(self.greenLightLabel)
        
        self.depthValueLabel = QLabel("Depth Value: ", self)
        self.layout.addWidget(self.depthValueLabel)
        
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

    def displayImage(self, imagepath):
        ''' 이미지 UI에 띄우기 '''
        pixmap = QPixmap(imagepath)
        self.label.setPixmap(pixmap)

    def new_connection(self):
        ''' 새로운 연결이 생길 시 작동 '''
        client_connection = self.tcpServer.nextPendingConnection() # 큐에서 대기 중인 클라이언트 연결 가져오기
        client_connection.readyRead.connect(self.receive_data)
        
    def receive_data(self):
        ''' 데이터가 들어올 시, json 파싱 & 디코딩 '''
        client_connection = self.sender()
        if client_connection:
            data = client_connection.readAll().data().decode()
            if data:
                try:
                    received_data = json.loads(data)
                    self.handle_data(received_data)
                except json.JSONDecodeError as e:
                    self.label.setText(f"JSON decode error: {e}")
            else:
                self.label.setText("No data received")
                
    def handle_data(self, received_data):
        ''' 받은 데이터로 작업 수행 '''
        left_sign_detected = received_data.get("left_sign_detected", "Unknown")
        current_green_light = received_data.get("current_green_light", "Unknown")
        depth_value = received_data.get("depth_value", -1)

        # UI 업데이트
        # self.leftSignLabel.setText(f"Left Sign Detected: {left_sign_detected}")
        # self.greenLightLabel.setText(f"Current Green Light: {current_green_light}")
        # self.depthValueLabel.setText(f"Depth Value: {depth_value}")
        
        # 각 키의 값에 따른 행동
        if left_sign_detected and not current_green_light:
            print("---Nope---")

        elif left_sign_detected and current_green_light:
            if depth_value < 0:
                print("-----wait-----")
            elif depth_value >= 200:
                print("Danger!!!!!!!!!!!")
                # self.displayImage('/home/ubuntu/intel_project_left_sign/otx/data/unprotected.jpg')
            elif 0 <= depth_value < 200:
                print("~~Safe~~")
                # self.displayImage('/home/ubuntu/intel_project_left_sign/otx/data/Untitled.png')

        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ServerWindow()
    window.show()
    sys.exit(app.exec_()) # app.exec_() -> 이벤트 루프임. 종료 전까지 계속 실행됨


