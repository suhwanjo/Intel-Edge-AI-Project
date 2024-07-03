import logging
import threading
import queue
import cv2
import socket
import json

from traffic_sign_detection import TrafficSignDetection
from vehicle_detection import VehicleDetection

class VideoProcessor:
    def __init__(self, video_path, model_depth_xml_path, model_detection_xml_path, model_traffic_xml_path, raspberry_pi_ip, port=5001):
        self.video_path = video_path
        self.traffic_sign_detection = TrafficSignDetection(model_traffic_xml_path)
        self.vehicle_detection = VehicleDetection(model_detection_xml_path, model_depth_xml_path)
        self.frame_queue = queue.Queue(maxsize=30)
        self.traffic_frame_queue = queue.Queue(maxsize=1)
        self.traffic_result_queue = queue.Queue(maxsize=1)
        self.distance_frame_queue = queue.Queue(maxsize=1)
        self.distance_result_queue = queue.Queue(maxsize=1)
        self.frame_count = 0
        self.process_interval = 3
        self.raspberry_pi_ip = raspberry_pi_ip
        self.port = port

    def frame_capture(self):
        cap = cv2.VideoCapture(self.video_path)
        while True:
            ret, frame = cap.read()
            if not ret:
                logging.info("End of video stream")
                break

            if self.frame_queue.full():
                try:
                    self.frame_queue.get_nowait()
                except queue.Empty:
                    pass
            self.frame_queue.put(frame)

        cap.release()
        logging.info("Frame capture thread ended")
        self.frame_queue.put(None)  # 종료 신호로 None을 큐에 넣음

    def send_data_to_raspberry_pi(self, data):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.raspberry_pi_ip, self.port))

        data["depth_value"] = float(data["depth_value"])
        data_string = json.dumps(data)
        client_socket.sendall(data_string.encode('utf-8'))

        client_socket.close()

    def run(self):
        capture_thread = threading.Thread(target=self.frame_capture)
        traffic_thread = threading.Thread(target=self.traffic_sign_detection.detect, args=(self.traffic_frame_queue, self.traffic_result_queue))
        distance_thread = threading.Thread(target=self.vehicle_detection.measure_distance, args=(self.distance_frame_queue, self.distance_result_queue))

        capture_thread.start()
        traffic_thread.start()
        distance_thread.start()

        while True:
            try:
                frame = self.frame_queue.get(timeout=1)
                if frame is None:  # 종료 신호 확인
                    break
            except queue.Empty:
                continue

            self.frame_count += 1
            if self.frame_count % self.process_interval == 0:
                cropped_frame2 = frame[:, :int(frame.shape[1] * 0.52)]

                self.traffic_frame_queue.put(frame)
                try:
                    left_sign_detected, current_green_light, boxes, confidences, class_ids = self.traffic_result_queue.get(timeout=0.1)
                except queue.Empty:
                    continue

                if left_sign_detected and current_green_light:
                    self.distance_frame_queue.put(cropped_frame2)
                    try:
                        _, bounding_box, depth_value = self.distance_result_queue.get(timeout=0.1)
                        if bounding_box:
                            if depth_value:
                                data = {
                                    "left_sign_detected": left_sign_detected,
                                    "current_green_light": current_green_light,
                                    "depth_value": depth_value
                                }
                                print(data)
                                self.send_data_to_raspberry_pi(data)
                    except queue.Empty:
                        pass
                else:
                    data = {
                        "left_sign_detected": left_sign_detected,
                        "current_green_light": current_green_light,
                        "depth_value": 0
                    }
                    print(data)
                    self.send_data_to_raspberry_pi(data)

            cv2.imshow('Detection Results', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.traffic_frame_queue.put(None)
        self.distance_frame_queue.put(None)

        capture_thread.join()
        traffic_thread.join()
        distance_thread.join()

        cv2.destroyAllWindows()

