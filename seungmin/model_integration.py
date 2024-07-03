import cv2
import numpy as np
import time
from openvino.runtime import Core

class BoundingBox:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin, self.ymin, self.xmax, self.ymax = xmin, ymin, xmax, ymax
        self.miss_cnt = 0
        self.max_value = 0

    def miss_count(self):
        self.miss_cnt += 1

def update_bounding_box(bounding_box, xmin, ymin, xmax, ymax):
    bounding_box.xmin, bounding_box.ymin, bounding_box.xmax, bounding_box.ymax = xmin, ymin, xmax, ymax

def draw_boxes(image, boxes, confidences, class_ids, classes, conf_threshold=0.5):
    for i in range(len(boxes)):
        if confidences[i] > conf_threshold:
            x_min, y_min, x_max, y_max = boxes[i]
            confidence = confidences[i]
            label = f"{classes[class_ids[i]]}: {confidence:.2f}"
            color = (0, 255, 0)
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)
            cv2.putText(image, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

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

def load_model(model_xml):
    ie = Core()
    model = ie.read_model(model=model_xml)
    compiled_model = ie.compile_model(model=model, device_name="CPU")
    return compiled_model

def infer_frame(compiled_model, frame, input_size=(640, 640)):
    original_height, original_width = frame.shape[:2]
    resized_image = cv2.resize(frame, input_size)
    input_data = np.expand_dims(resized_image.transpose(2, 0, 1), axis=0).astype(np.float16)

    results = compiled_model([input_data])
    boxes = results[0][0]
    labels = results[1][0]

    parsed_boxes = []
    confidences = []
    class_ids = []
    for box, label in zip(boxes, labels):
        x_min, y_min, x_max, y_max, confidence = box
        if confidence > 0.7:
            x_min = int(x_min * original_width / input_size[0])
            y_min = int(y_min * original_height / input_size[1])
            x_max = int(x_max * original_width / input_size[0])
            y_max = int(y_max * original_height / input_size[1])
            parsed_boxes.append([x_min, y_min, x_max, y_max])
            confidences.append(float(confidence))
            class_ids.append(int(label))
    return parsed_boxes, confidences, class_ids

def detect_and_measure_vehicle(frame, bounding_box, compiled_model_detection, compiled_model_depth):
    cropped_frame = frame[:, :int(frame.shape[1] * 0.53)]
    resized_image_detection = cv2.resize(cropped_frame, (672, 384))
    input_image_detection = np.expand_dims(resized_image_detection.transpose(2, 0, 1), axis=0).astype(np.float16)

    result_detection = compiled_model_detection([input_image_detection])[0]

    center_x, center_y = 0, 0
    max_y = 0
    for detection in result_detection[0][0]:
        confidence = detection[2]
        if confidence > 0.5:
            xmin = int(detection[3] * cropped_frame.shape[1])
            ymin = int(detection[4] * cropped_frame.shape[0])
            xmax = int(detection[5] * cropped_frame.shape[1])
            ymax = int(detection[6] * cropped_frame.shape[0])
            
            if max_y < ymax:
                max_y = ymax
                if bounding_box is None:
                    bounding_box = BoundingBox(xmin, ymin, xmax, ymax)
                else:
                    if bounding_box.ymax > max_y:
                        bounding_box.miss_count()
                    else:
                        update_bounding_box(bounding_box, xmin, ymin, xmax, ymax)
                        bounding_box.miss_cnt = 0
    
    if bounding_box.miss_cnt > 10:
        update_bounding_box(bounding_box, 0, 0, 0, 0)
        bounding_box.miss_cnt = 0
    else:
        center_x = (bounding_box.xmin + bounding_box.xmax) // 2
        center_y = (bounding_box.ymin + bounding_box.ymax) // 2
        cv2.rectangle(frame, (bounding_box.xmin, bounding_box.ymin), (bounding_box.xmax, bounding_box.ymax), (0, 255, 0), 2)

        resized_image_depth = cv2.resize(frame, (256, 256))
        input_image_depth = np.expand_dims(resized_image_depth.transpose(2, 0, 1), axis=0).astype(np.float16)
        result_depth = compiled_model_depth([input_image_depth])[0]
        
        result_depth_rescaled = cv2.resize(result_depth[0], (frame.shape[1], frame.shape[0]))
        
        depth_value = result_depth_rescaled[center_y, center_x]
        cv2.putText(frame, f'Distance: {depth_value:.2f}', (bounding_box.xmin, bounding_box.ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
        if depth_value > 100.0:
            cv2.putText(frame, 'Danger!!', (frame.shape[1] // 4, frame.shape[0] // 2), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 4)
    
    return frame, bounding_box

def main(video_path, model_depth_xml_path, model_detection_xml_path, model_traffic_xml_path):
    classes = ['left_traffic_sign', 'traffic_light']
    
    compiled_model_depth = load_model(model_depth_xml_path)
    compiled_model_detection = load_model(model_detection_xml_path)
    compiled_model_traffic = load_model(model_traffic_xml_path)
    
    cap = cv2.VideoCapture(video_path)

    bounding_box = None
    prev_green_light = False

    total_start_time = time.time()  # 전체 실행 시간 측정 시작

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_start_time = time.time()  # 각 프레임 처리 시간 측정 시작
        
        parsed_boxes, confidences, class_ids = infer_frame(compiled_model_traffic, frame)
        draw_boxes(frame, parsed_boxes, confidences, class_ids, classes)
        
        left_sign_detected = False
        current_green_light = False

        for i, class_id in enumerate(class_ids):
            if classes[class_id] == 'left_traffic_sign':
                left_sign_detected = True
            if classes[class_id] == 'traffic_light':
                color = extract_color(frame, parsed_boxes[i])
                print(f"신호등: {color}")
                if color == "green":
                    current_green_light = True

        if left_sign_detected and current_green_light and prev_green_light:
            frame, bounding_box = detect_and_measure_vehicle(frame, bounding_box, compiled_model_detection, compiled_model_depth)

        frame_end_time = time.time()  # 각 프레임 처리 시간 측정 종료
       # print(f"Frame processing time: {frame_end_time - frame_start_time:.4f} seconds")

        cv2.imshow('Detection Results', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        prev_green_light = current_green_light

    total_end_time = time.time()  # 전체 실행 시간 측정 종료
    #print(f"Total processing time: {total_end_time - total_start_time:.4f} seconds")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = "/home/ubuntu/model/example.mp4"
    model_depth_xml_path = "/home/ubuntu/model/MiDaS_small.xml"
    model_detection_xml_path = "/home/ubuntu/model/vehicle-detection-adas-0002.xml"
    model_traffic_xml_path = "/home/ubuntu/model/openvino.xml"
    main(video_path, model_depth_xml_path, model_detection_xml_path, model_traffic_xml_path)