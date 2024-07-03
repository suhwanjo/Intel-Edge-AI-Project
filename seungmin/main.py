from video_processor import VideoProcessor

if __name__ == "__main__":
    video_path = "MAN_20240621_185159_F.MP4"#"http://192.168.0.101:8081"
    model_depth_xml_path = "models/MiDaS_small.xml"
    model_detection_xml_path = "models/vehicle-detection-adas-0002.xml"
    model_traffic_xml_path = "models/pot2/openvino.xml"
    raspberry_pi_ip = "192.168.0.101"  # 라즈베리파이의 IP 주소
    processor = VideoProcessor(video_path, model_depth_xml_path, model_detection_xml_path, model_traffic_xml_path, raspberry_pi_ip)
    processor.run()
