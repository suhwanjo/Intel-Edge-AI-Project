import cv2
import numpy as np
from openvino.runtime import Core

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

        # Calculate average brightness (V channel)
        segment_brightness = np.mean(segment[:, :, 2])
        if i == 0 and segment_brightness > 210 and color != "green":
            color = "red"
        if i == 1 and segment_brightness > 200:
            color = "yellow"
        if i == 3 and segment_brightness > 170 and color != "red":
            color = "green"

    return color

def load_model(model_xml, model_bin):
    ie = Core()
    model = ie.read_model(model=model_xml, weights=model_bin)
    compiled_model = ie.compile_model(model=model, device_name="CPU")
    return compiled_model

def infer_frame(compiled_model, frame, input_size=(640, 640)):
    original_height, original_width = frame.shape[:2]
    image_resized = cv2.resize(frame, input_size)
    input_data = np.expand_dims(image_resized.transpose(2, 0, 1), axis=0).astype(np.float32)

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

def main(video_path, model_xml, model_bin):
    classes = ['left_traffic_sign', 'traffic_light']
    compiled_model = load_model(model_xml, model_bin)
    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        parsed_boxes, confidences, class_ids = infer_frame(compiled_model, frame)
        draw_boxes(frame, parsed_boxes, confidences, class_ids, classes)

        for i, class_id in enumerate(class_ids):
            if classes[class_id] == 'traffic_light':
                colors = extract_color(frame, parsed_boxes[i])
                print(f"Traffic light colors: {colors}")

        cv2.imshow("Detection Results", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = "MAN_20240621_185159_F.MP4"
    model_xml = "outputs/pot2/openvino.xml"
    model_bin = "outputs/pot2/openvino.bin"
    main(video_path, model_xml, model_bin)
