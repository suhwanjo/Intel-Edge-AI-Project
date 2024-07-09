import cv2
import numpy as np
from openvino.runtime import Core

class TrafficSignDetection:
    def __init__(self, model_path):
        # Initialize the model with the provided path
        self.compiled_model = self.load_model(model_path)
        # Define the input size for the model
        self.input_size = (640, 640)
        # Define the classes that the model can detect
        self.classes = ['left_traffic_sign', 'traffic_light']
        # Initialize the previous green light state
        self.prev_green_light = False

    def load_model(self, model_xml):
        # Load and compile the OpenVINO model
        ie = Core()
        model = ie.read_model(model=model_xml)
        compiled_model = ie.compile_model(model=model, device_name="CPU")
        return compiled_model

    def preprocess_frame(self, frame):
        # Resize the frame to match the input size of the model
        resized = cv2.resize(frame, self.input_size)
        # Rearrange the dimensions and convert the data type
        return np.expand_dims(resized.transpose(2, 0, 1), axis=0).astype(np.float16)

    def extract_color(self, image, box):
        # Extract the region of interest based on the bounding box
        x_min, y_min, x_max, y_max = box
        crop_img = image[y_min:y_max, x_min:x_max]
        # Convert the cropped image to HSV color space
        hsv_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
        height, width, _ = hsv_img.shape
        segment_width = width // 4

        # Initialize the color as "none"
        color = "none"
        segment_list = []
        # Divide the image into 4 vertical segments and calculate the brightness
        for i in range(4):
            segment_x_start = i * segment_width
            segment_x_end = (i + 1) * segment_width
            segment = hsv_img[:, segment_x_start:segment_x_end]
            segment_brightness = np.mean(segment[:, :, 2])
            segment_list.append(segment_brightness) 
        
        # Determine the color based on the segment with the highest brightness
        max_index = np.argmax(segment_list)
        if max_index == 0 and color != "green":
            color = "red"
        if max_index == 1:
            color = "yellow"
        if max_index == 3 and color != "red":
            color = "green"
        
        return color

    def postprocess_traffic_detection(self, boxes, labels, frame_shape, conf_threshold=0.65):
        # Postprocess the model outputs to filter detections based on confidence
        parsed_boxes = []
        confidences = []
        class_ids = []
        for box, label in zip(boxes, labels):
            confidence = box[4]
            if confidence > conf_threshold:
                # Convert the box coordinates to the original frame size
                xmin = int(box[0] * frame_shape[1] / self.input_size[0])
                ymin = int(box[1] * frame_shape[0] / self.input_size[1])
                xmax = int(box[2] * frame_shape[1] / self.input_size[0])
                ymax = int(box[3] * frame_shape[0] / self.input_size[1])
                parsed_boxes.append([xmin, ymin, xmax, ymax])
                confidences.append(float(confidence))
                class_ids.append(int(label))
        return parsed_boxes, confidences, class_ids

    def detect(self, frame_queue, result_queue):
        # Continuously process frames from the frame queue
        while True:
            frame = frame_queue.get()
            if frame is None:
                break

            # Preprocess the frame for the model
            input_data = self.preprocess_frame(frame)
            # Perform inference using the compiled model
            results = self.compiled_model([input_data])
            # Postprocess the model outputs
            parsed_boxes, confidences, class_ids = self.postprocess_traffic_detection(results[0][0], results[1][0], frame.shape)
            left_sign_detected = False
            current_green_light = False

            # Analyze the detected objects
            for i, class_id in enumerate(class_ids):
                if self.classes[class_id] == 'left_traffic_sign':
                    left_sign_detected = True
                if self.classes[class_id] == 'traffic_light':
                    color = self.extract_color(frame, parsed_boxes[i])
                    if color == "green":
                        current_green_light = True

            # Put the detection results into the result queue
            result_queue.put((left_sign_detected, current_green_light, parsed_boxes, confidences, class_ids))
