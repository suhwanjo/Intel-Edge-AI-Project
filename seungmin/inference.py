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

    colors = ["none", "none", "none", "none"]

    for i in range(4):
        segment_x_start = i * segment_width
        segment_x_end = (i + 1) * segment_width
        segment = hsv_img[:, segment_x_start:segment_x_end]

        segment_brightness = np.mean(segment[:, :, 2])
        if segment_brightness > 200:
            if i == 0:
                colors[0] = "red"
            elif i == 1:
                colors[1] = "yellow"
            elif i in [2, 3]:
                colors[i] = "green"

    return colors

classes = ['left_traffic_sign', 'traffic_light']

model_xml = "/home/ubuntu/project_Turn/tiny/model/model.xml"
model_bin = "/home/ubuntu/project_Turn/tiny/model/model.bin"

ie = Core()

model = ie.read_model(model=model_xml, weights=model_bin)
compiled_model = ie.compile_model(model=model, device_name="CPU")

for output in compiled_model.outputs:
    print(f"Name: {output.any_name}, Type: {output.element_type}")

output_boxes = compiled_model.output("boxes")
output_labels = compiled_model.output("labels")

cap = cv2.VideoCapture("/home/ubuntu/project_Turn/MAN_20240621_185159_F.MP4")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame.")
        break

    original_height, original_width = frame.shape[:2]
    image_resized = cv2.resize(frame, (640, 640))
    input_data = np.expand_dims(image_resized.transpose(2, 0, 1), axis=0).astype(np.float32)

    results = compiled_model([input_data])
    boxes = results[0][0]
    labels = results[1][0]

    parsed_boxes = []
    confidences = []
    class_ids = []
    for box, label in zip(boxes, labels):
        x_min, y_min, x_max, y_max, confidence = box
        if confidence > 0.5:
            x_min = int(x_min * original_width / 640)
            y_min = int(y_min * original_height / 640)
            x_max = int(x_max * original_width / 640)
            y_max = int(y_max * original_height / 640)
            parsed_boxes.append([x_min, y_min, x_max, y_max])
            confidences.append(float(confidence))
            class_ids.append(int(label))

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
