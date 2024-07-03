import cv2
import numpy as np
from openvino.runtime import Core

class BoundingBox:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin, self.ymin, self.xmax, self.ymax = xmin, ymin, xmax, ymax
        self.miss_cnt = 0

class VehicleDetection:
    def __init__(self, model_detection_path, model_depth_path):
        self.compiled_model_detection = self.load_model(model_detection_path)
        self.compiled_model_depth = self.load_model(model_depth_path)
        self.input_size_detection = (672, 384)
        self.input_size_depth = (256, 256)
        self.bounding_box = None

    def load_model(self, model_xml):
        ie = Core()
        model = ie.read_model(model=model_xml)
        compiled_model = ie.compile_model(model=model, device_name="CPU")
        return compiled_model

    def preprocess_frame(self, frame, input_size):
        resized = cv2.resize(frame, input_size)
        return np.expand_dims(resized.transpose(2, 0, 1), axis=0).astype(np.float16)

    def postprocess_vehicle_detection(self, output, frame_shape, conf_threshold=0.5):
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

    def detect_and_measure_vehicle(self, frame):
        input_data = self.preprocess_frame(frame, self.input_size_detection)
        result = self.compiled_model_detection([input_data])[0]

        boxes, confidences, _ = self.postprocess_vehicle_detection(result, frame.shape)

        if boxes:
            box = max(boxes, key=lambda b: b[3])  # Get the box with the largest y-max
            if self.bounding_box is None:
                self.bounding_box = BoundingBox(*box)
            else:
                if box[3] > self.bounding_box.ymax:
                    self.bounding_box.xmin, self.bounding_box.ymin, self.bounding_box.xmax, self.bounding_box.ymax = box
                    self.bounding_box.miss_cnt = 0
                else:
                    self.bounding_box.miss_cnt += 1
        else:
            if self.bounding_box:
                self.bounding_box.miss_cnt += 1

        if self.bounding_box and self.bounding_box.miss_cnt <= 10:
            center_x = (self.bounding_box.xmin + self.bounding_box.xmax) // 2
            center_y = (self.bounding_box.ymin + self.bounding_box.ymax) // 2

            depth_input = self.preprocess_frame(frame, self.input_size_depth)
            depth_result = self.compiled_model_depth([depth_input])[0]
            depth_result_rescaled = cv2.resize(depth_result[0], (frame.shape[1], frame.shape[0]))
            depth_value = depth_result_rescaled[center_y, center_x]

            return frame, self.bounding_box, depth_value

        return frame, None, None

    def measure_distance(self, frame_queue, result_queue):
        while True:
            frame = frame_queue.get()
            if frame is None:
                break

            frame, bounding_box, depth_value = self.detect_and_measure_vehicle(frame)
            result_queue.put((frame, bounding_box, depth_value))
