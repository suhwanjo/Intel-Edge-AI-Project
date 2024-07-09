from video_processor import VideoProcessor

if __name__ == "__main__":
    # Get the Raspberry Pi IP address from the user
    raspberry_pi_ip = input("Please enter the Raspberry Pi IP address: ")

    # Set the video path and model paths
    video_path = "http://192.168.245.236:8081"
    model_depth_xml_path = "models/MiDaS_small.xml"
    model_detection_xml_path = "models/vehicle-detection-adas-0002.xml"
    model_traffic_xml_path = "models/pot2/openvino.xml"

    # Create a VideoProcessor instance with the provided IP address
    processor = VideoProcessor(video_path, model_depth_xml_path, model_detection_xml_path, model_traffic_xml_path, raspberry_pi_ip)

    # Run the video processor
    processor.run()
