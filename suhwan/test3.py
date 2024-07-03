import cv2
import numpy as np
from openvino.runtime import Core
import threading
import queue
import logging
import time
logging.basicConfig(level=logging.INFO)

class BoundingBox:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin, self.ymin, self.xmax, self.ymax = xmin, ymin, xmax, ymax
        self.miss_cnt = 0

def load_model(model_xml):
    ie = Core()
    model = ie.read_model(model=model_xml)
    compiled_model = ie.compile_model(model=model, device_name="CPU")
    return compiled_model

def preprocess_frame(frame, input_size):
    resized = cv2.resize(frame, input_size)
    return np.expand_dims(resized.transpose(2, 0, 1), axis=0).astype(np.float16)

def extract_color(image, box):
    x_min, y_min, x_max, y_max = box
    crop_img = image[y_min:y_max, x_min:x_max]
    hsv_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
    height, width, _ = hsv_img.shape
    segment_width = width // 4

    color = "none"

    for i in range(4):
        segment_x_start = i * segment_width
        segment_x_end = (i + 1) * segment_width
        segment = hsv_img[:, segment_x_start:segment_x_end]

        segment_brightness = np.mean(segment[:, :, 2])
        if i == 0 and segment_brightness > 210 and color != "green":
            color = "red"
        if i == 1 and segment_brightness > 200:
            color = "yellow"
        if i == 3 and segment_brightness > 170 and color != "red":
            color = "green"

    return color

def postprocess_traffic_detection(boxes, labels, frame_shape, conf_threshold=0.5):
    input_size = (640, 640)
    parsed_boxes = []
    confidences = []
    class_ids = []
    for box, label in zip(boxes, labels):
        confidence = box[4]
        if confidence > conf_threshold:
            xmin = int(box[0] * frame_shape[1] / input_size[0])
            ymin = int(box[1] * frame_shape[0]/ input_size[1])
            xmax = int(box[2] * frame_shape[1]/ input_size[0])
            ymax = int(box[3] * frame_shape[0]/ input_size[1])
            parsed_boxes.append([xmin, ymin, xmax, ymax])
            confidences.append(float(confidence))
            class_ids.append(int(label))
    return parsed_boxes, confidences, class_ids

def postprocess_vehicle_detection(output, frame_shape, conf_threshold=0.5):
    boxes = []
    confidences = []
    class_ids = []
    for detection in output[0][0]:
        confidence = detection[2]
        if confidence > conf_threshold:
            xmin = int(detection[3] * frame_shape[1])
            ymin = int(detection[4] * frame_shape[0])
            xmax = int(detection[5] * frame_shape[1])
            ymax = int(detection[6] * frame_shape[0])
            boxes.append([xmin, ymin, xmax, ymax])
            confidences.append(float(confidence))
            class_ids.append(int(detection[1]))
    return boxes, confidences, class_ids


def traffic_sign_detection(frame_queue, result_queue, compiled_model):
    input_size = (640, 640)
    classes = ['left_traffic_sign', 'traffic_light']

    while True:
        frame = frame_queue.get()
        if frame is None:
            break

        input_data = preprocess_frame(frame, input_size)
        results = compiled_model([input_data])
        parsed_boxes, confidences, class_ids = postprocess_traffic_detection(results[0][0], results[1][0], frame.shape)
        left_sign_detected = False
        current_green_light = False

        for i, class_id in enumerate(class_ids):
            if classes[class_id] == 'left_traffic_sign':
                left_sign_detected = True
            if classes[class_id] == 'traffic_light':
                color = extract_color(frame, parsed_boxes[i])
                if color == "green":
                    current_green_light = True
                    print("Green")


        result_queue.put((left_sign_detected, current_green_light, parsed_boxes, confidences, class_ids))

def detect_and_measure_vehicle(frame, bounding_box, compiled_model_detection, compiled_model_depth):
    input_size = (672, 384)

    input_data = preprocess_frame(frame, input_size)
    result = compiled_model_detection([input_data])[0]
    
    boxes, confidences, _ = postprocess_vehicle_detection(result, frame.shape)
    
    if boxes:
        box = max(boxes, key=lambda b: b[3])  # Get the box with the largest y-max
        if bounding_box is None:
            bounding_box = BoundingBox(*box)
        else:
            if box[3] > bounding_box.ymax:
                bounding_box.xmin, bounding_box.ymin, bounding_box.xmax, bounding_box.ymax = box
                bounding_box.miss_cnt = 0
            else:
                bounding_box.miss_cnt += 1
    else:
        if bounding_box:
            bounding_box.miss_cnt += 1
    
    if bounding_box and bounding_box.miss_cnt <= 10:
        center_x = (bounding_box.xmin + bounding_box.xmax) // 2
        center_y = (bounding_box.ymin + bounding_box.ymax) // 2
        
        depth_input = preprocess_frame(frame, (256, 256))
        depth_result = compiled_model_depth([depth_input])[0]
        depth_result_rescaled = cv2.resize(depth_result[0], (frame.shape[1], frame.shape[0]))
        depth_value = depth_result_rescaled[center_y, center_x]
        
        return frame, bounding_box, depth_value
    
    return frame, None, None

def distance_measurement(frame_queue, result_queue, compiled_model_detection, compiled_model_depth):
    bounding_box = None
    while True:
        frame = frame_queue.get()
        if frame is None:
            break
        
        frame, bounding_box, depth_value = detect_and_measure_vehicle(frame, bounding_box, compiled_model_detection, compiled_model_depth)
        result_queue.put((frame, bounding_box, depth_value))

def frame_capture(video_path, frame_queue):
    cap = cv2.VideoCapture(video_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            logging.info("End of video stream")
            break
        
        if frame_queue.full():
            try:
                frame_queue.get_nowait()
            except queue.Empty:
                pass
        frame_queue.put(frame)
    
    cap.release()
    logging.info("Frame capture thread ended")
    frame_queue.put(None)  # 종료 신호로 None을 큐에 넣음

def main(video_path, model_depth_xml_path, model_detection_xml_path, model_traffic_xml_path):
    compiled_model_depth = load_model(model_depth_xml_path)
    compiled_model_detection = load_model(model_detection_xml_path)
    compiled_model_traffic = load_model(model_traffic_xml_path)
    
    frame_queue = queue.Queue(maxsize=30)
    traffic_frame_queue = queue.Queue(maxsize=1)
    traffic_result_queue = queue.Queue(maxsize=1)
    distance_frame_queue = queue.Queue(maxsize=1)
    distance_result_queue = queue.Queue(maxsize=1)

    capture_thread = threading.Thread(target=frame_capture, args=(video_path, frame_queue))
    traffic_thread = threading.Thread(target=traffic_sign_detection, args=(traffic_frame_queue, traffic_result_queue, compiled_model_traffic))
    distance_thread = threading.Thread(target=distance_measurement, args=(distance_frame_queue, distance_result_queue, compiled_model_detection, compiled_model_depth))

    capture_thread.start()
    traffic_thread.start()
    distance_thread.start()

    frame_count = 0
    process_interval = 10  # Process every 10 frames

    while True:
        try:
            frame = frame_queue.get(timeout=1)
            if frame is None:  # 종료 신호 확인
                break
        except queue.Empty:
            continue

        frame_count += 1

        if frame_count % process_interval == 0:
            cropped_frame = frame[:, int(frame.shape[1] * 0.4):]
            cropped_frame2 = frame[:, :int(frame.shape[1] * 0.52)]

            traffic_frame_queue.put(cropped_frame)
            try:
                left_sign_detected, current_green_light, boxes, confidences, class_ids = traffic_result_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            # Always display traffic sign detection results
            #for box, conf, class_id in zip(boxes, confidences, class_ids):
                #cv2.imshow('Detection Results', cropped_frame)
                #cv2.rectangle(cropped_frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                #label = f"{'Left Sign' if class_id == 0 else 'Traffic Light'}: {conf:.2f}"
                #cv2.putText(cropped_frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if left_sign_detected and current_green_light:
                distance_frame_queue.put(cropped_frame2)
                try:
                    _, bounding_box, depth_value = distance_result_queue.get(timeout=0.1)
                    if bounding_box:
                        print("car")
                        #cv2.imshow('Detection Results', cropped_frame2)
                        #cv2.rectangle(cropped_frame2, (bounding_box.xmin, bounding_box.ymin), 
                        #              (bounding_box.xmax, bounding_box.ymax), (255, 0, 0), 2)
                        if depth_value:
                            #cv2.putText(cropped_frame2, f'Distance: {depth_value:.2f}', 
                            #            (bounding_box.xmin, bounding_box.ymin - 10), 
                            #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                            if depth_value > 50.0:
                                print("Danger!!!!!!!!!!!!!!!!!!")
                                #cv2.putText(cropped_frame2, "DANGER!", (50, 50), 
                                #            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                except queue.Empty:
                    pass


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 종료 신호 전송
    traffic_frame_queue.put(None)
    distance_frame_queue.put(None)

    # 스레드 종료 대기
    capture_thread.join()
    traffic_thread.join()
    distance_thread.join()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = "MAN_20240621_185159_F.MP4"
    model_depth_xml_path = "MiDaS_small.xml"
    model_detection_xml_path = "vehicle-detection-adas-0002.xml"
    model_traffic_xml_path = "outputs/pot2/openvino.xml"
    main(video_path, model_depth_xml_path, model_detection_xml_path, model_traffic_xml_path)