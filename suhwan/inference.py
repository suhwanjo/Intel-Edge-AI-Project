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

# COCO 클래스 이름 로드
classes = ['left_traffic_sign', 'traffic_light']

# 모델과 가중치 파일 경로
model_xml = "otx-workspace-DETECTION/outputs/pot/openvino.xml"
model_bin = "otx-workspace-DETECTION/outputs/pot/openvino.bin"

# OpenVINO Inference Engine 초기화
ie = Core()

# 모델 로드 및 컴파일
model = ie.read_model(model=model_xml, weights=model_bin)
compiled_model = ie.compile_model(model=model, device_name="CPU")

# 모든 출력 레이어 확인
for output in compiled_model.outputs:
    print(f"Name: {output.any_name}, Type: {output.element_type}")

# 출력 레이어 가져오기
output_boxes = compiled_model.output("boxes")
output_labels = compiled_model.output("labels")

# 이미지 로드 및 전처리
image = cv2.imread("inference_test.png")
original_height, original_width = image.shape[:2]
image_resized = cv2.resize(image, (640, 640))  # 모델 입력 크기에 맞춤
input_data = np.expand_dims(image_resized.transpose(2, 0, 1), axis=0).astype(np.float32)

# 추론 실행
results = compiled_model([input_data])
boxes = results[0][0]
labels = results[1][0]

# 결과 해석 (박스 좌표, 신뢰도, 클래스 ID)
parsed_boxes = []
confidences = []
class_ids = []
for box, label in zip(boxes, labels):
    x_min, y_min, x_max, y_max, confidence = box
    if confidence > 0:  # 신뢰도가 0보다 큰 경우만 고려
        x_min = int(x_min * original_width / 640)
        y_min = int(y_min * original_height / 640)
        x_max = int(x_max * original_width / 640)
        y_max = int(y_max * original_height / 640)
        parsed_boxes.append([x_min, y_min, x_max, y_max])
        confidences.append(float(confidence))
        class_ids.append(int(label))

# 박스 그리기
draw_boxes(image, parsed_boxes, confidences, class_ids, classes)

# 결과 이미지 저장 또는 표시
cv2.imshow("Detection Results", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("output.png", image)
