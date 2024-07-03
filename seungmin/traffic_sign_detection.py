import cv2
import numpy as np
from openvino.runtime import Core

class TrafficSignDetection:
    def __init__(self, model_path):
        self.compiled_model = self.load_model(model_path)
        self.input_size = (640, 640)
        self.classes = ['left_traffic_sign', 'traffic_light']
        self.prev_green_light = False

    def load_model(self, model_xml):
        ie = Core()
        model = ie.read_model(model=model_xml)
        compiled_model = ie.compile_model(model=model, device_name="CPU")
        return compiled_model

    def preprocess_frame(self, frame):
        resized = cv2.resize(frame, self.input_size)
        return np.expand_dims(resized.transpose(2, 0, 1), axis=0).astype(np.float16)

    def extract_color(self, image, box):
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

    def postprocess_traffic_detection(self, boxes, labels, frame_shape, conf_threshold=0.6):
        parsed_boxes = []
        confidences = []
        class_ids = []
        for box, label in zip(boxes, labels):
            confidence = box[4]
            if confidence > conf_threshold:
                xmin = int(box[0] * frame_shape[1] / self.input_size[0])
                ymin = int(box[1] * frame_shape[0] / self.input_size[1])
                xmax = int(box[2] * frame_shape[1] / self.input_size[0])
                ymax = int(box[3] * frame_shape[0] / self.input_size[1])
                parsed_boxes.append([xmin, ymin, xmax, ymax])
                confidences.append(float(confidence))
                class_ids.append(int(label))
        return parsed_boxes, confidences, class_ids

    def detect(self, frame_queue, result_queue):
        while True:
            frame = frame_queue.get()
            if frame is None:
                break

            input_data = self.preprocess_frame(frame)
            results = self.compiled_model([input_data])
            parsed_boxes, confidences, class_ids = self.postprocess_traffic_detection(results[0][0], results[1][0], frame.shape)
            left_sign_detected = False
            current_green_light = False

            for i, class_id in enumerate(class_ids):
                if self.classes[class_id] == 'left_traffic_sign':
                    left_sign_detected = True
                if self.classes[class_id] == 'traffic_light':
                    color = self.extract_color(frame, parsed_boxes[i])
                    if color == "green":
                        current_green_light = True

            final_green_light = self.prev_green_light and current_green_light
            self.prev_green_light = current_green_light

            result_queue.put((left_sign_detected, final_green_light, parsed_boxes, confidences, class_ids))
