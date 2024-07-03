# # import cv2
# # import numpy as np
# # from openvino.runtime import Core

# # def draw_boxes(image, boxes, confidences, class_ids, classes, conf_threshold=0.5):
# #     for i in range(len(boxes)):
# #         if confidences[i] > conf_threshold:
# #             x_min, y_min, x_max, y_max = boxes[i]
# #             confidence = confidences[i]
# #             label = f"{classes[class_ids[i]]}: {confidence:.2f}"
# #             color = (0, 255, 0)
# #             cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)
# #             cv2.putText(image, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# # def extract_color(image, box):
# #     x_min, y_min, x_max, y_max = box
# #     crop_img = image[y_min:y_max, x_min:x_max]
# #     hsv_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
# #     height, width, _ = hsv_img.shape
# #     segment_width = width // 4

# #     colors = ["none", "none", "none", "none"]

# #     for i in range(4):
# #         segment_x_start = i * segment_width
# #         segment_x_end = (i + 1) * segment_width
# #         segment = hsv_img[:, segment_x_start:segment_x_end]

# #         # Segment의 밝기(V 채널) 평균 계산
# #         segment_brightness = np.mean(segment[:, :, 2])  # V 채널의 평균 밝기
# #         if segment_brightness > 200:  # 밝기 임계값 설정
# #             if i == 0:
# #                 colors[0] = "red"
# #             elif i == 1:
# #                 colors[1] = "yellow"
# #             elif i in [2, 3]:
# #                 colors[i] = "green"

# #     return colors

# # # COCO 클래스 이름 로드
# # classes = ['left_traffic_sign', 'traffic_light']

# # # 모델과 가중치 파일 경로
# # model_xml = "model/model.xml"
# # model_bin = "model/model.bin"

# # # OpenVINO Inference Engine 초기화
# # ie = Core()

# # # 모델 로드 및 컴파일
# # model = ie.read_model(model=model_xml, weights=model_bin)
# # compiled_model = ie.compile_model(model=model, device_name="CPU")

# # # 모든 출력 레이어 확인
# # for output in compiled_model.outputs:
# #     print(f"Name: {output.any_name}, Type: {output.element_type}")

# # # 출력 레이어 가져오기
# # output_boxes = compiled_model.output("boxes")
# # output_labels = compiled_model.output("labels")

# # # 웹캠 초기화
# # cap = cv2.VideoCapture("MAN_20240621_185159_F.MP4")  # Using webcam

# # while True:
# #     ret, frame = cap.read()
# #     if not ret:
# #         break

# #     original_height, original_width = frame.shape[:2]
# #     image_resized = cv2.resize(frame, (640, 640))  # 모델 입력 크기에 맞춤
# #     input_data = np.expand_dims(image_resized.transpose(2, 0, 1), axis=0).astype(np.float32)

# #     # 추론 실행
# #     results = compiled_model([input_data])
# #     boxes = results[0][0]
# #     labels = results[1][0]

# #     # 결과 해석 (박스 좌표, 신뢰도, 클래스 ID)
# #     parsed_boxes = []
# #     confidences = []
# #     class_ids = []
# #     for box, label in zip(boxes, labels):
# #         x_min, y_min, x_max, y_max, confidence = box
# #         if confidence > 0.5:  # 신뢰도가 0.5보다 큰 경우만 고려
# #             x_min = int(x_min * original_width / 640)
# #             y_min = int(y_min * original_height / 640)
# #             x_max = int(x_max * original_width / 640)
# #             y_max = int(y_max * original_height / 640)
# #             parsed_boxes.append([x_min, y_min, x_max, y_max])
# #             confidences.append(float(confidence))
# #             class_ids.append(int(label))

# #     # 박스 그리기
# #     draw_boxes(frame, parsed_boxes, confidences, class_ids, classes)

# #     # 특정 클래스(traffic_light) 색상 추출
# #     for i, class_id in enumerate(class_ids):
# #         if classes[class_id] == 'traffic_light':
# #             colors = extract_color(frame, parsed_boxes[i])
# #             print(f"Traffic light colors: {colors}")

# #     # 결과 이미지 표시
# #     cv2.imshow("Detection Results", frame)
    
# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break

# # # 웹캠 릴리즈 및 윈도우 닫기
# # cap.release()
# # cv2.destroyAllWindows()
# import cv2
# import numpy as np
# from openvino.runtime import Core

# def draw_boxes(image, boxes, confidences, class_ids, classes, conf_threshold=0.5):
#     for i in range(len(boxes)):
#         if confidences[i] > conf_threshold:
#             x_min, y_min, x_max, y_max = boxes[i]
#             confidence = confidences[i]
#             label = f"{classes[class_ids[i]]}: {confidence:.2f}"
#             color = (0, 255, 0)
#             cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)
#             cv2.putText(image, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# def extract_color(image, box):
#     x_min, y_min, x_max, y_max = box
#     crop_img = image[y_min:y_max, x_min:x_max]
#     hsv_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
#     height, width, _ = hsv_img.shape
#     segment_width = width // 4

#     colors = ["none", "none", "none", "none"]

#     for i in range(4):
#         segment_x_start = i * segment_width
#         segment_x_end = (i + 1) * segment_width
#         segment = hsv_img[:, segment_x_start:segment_x_end]

#         # Segment의 밝기(V 채널) 평균 계산
#         segment_brightness = np.mean(segment[:, :, 2])  # V 채널의 평균 밝기
#         if segment_brightness > 200:  # 밝기 임계값 설정
#             if i == 0:
#                 colors[0] = "red"
#             elif i == 1:
#                 colors[1] = "yellow"
#             elif i in [2, 3]:
#                 colors[i] = "green"

#     return colors

# def adjust_gamma(image, gamma=1.0):
#     inv_gamma = 1.0 / gamma
#     table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
#     return cv2.LUT(image, table)

# # COCO 클래스 이름 로드
# classes = ['left_traffic_sign', 'traffic_light']

# # 모델과 가중치 파일 경로
# model_xml = "model/model.xml"
# model_bin = "model/model.bin"

# # OpenVINO Inference Engine 초기화
# ie = Core()

# # 모델 로드 및 컴파일
# model = ie.read_model(model=model_xml, weights=model_bin)
# compiled_model = ie.compile_model(model=model, device_name="CPU")

# # 웹캠 초기화
# cap = cv2.VideoCapture("MAN_20240621_185159_F.MP4")  # Using webcam

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     original_height, original_width = frame.shape[:2]
#     image_resized = cv2.resize(frame, (640, 640))  # 모델 입력 크기에 맞춤
#        # Gamma 보정을 적용하여 이미지 밝기 조정
#     gamma_corrected_image = adjust_gamma(image_resized, gamma=0.5)

#     input_data = np.expand_dims(gamma_corrected_image.transpose(2, 0, 1), axis=0).astype(np.float32)

#     # 추론 실행
#     results = compiled_model([input_data])
#     boxes = results[0][0]
#     labels = results[1][0]

#     # 결과 해석 (박스 좌표, 신뢰도, 클래스 ID)
#     parsed_boxes = []
#     confidences = []
#     class_ids = []
#     for box, label in zip(boxes, labels):
#         x_min, y_min, x_max, y_max, confidence = box
#         if confidence > 0.5:  # 신뢰도가 0.5보다 큰 경우만 고려
#             x_min = int(x_min * original_width / 640)
#             y_min = int(y_min * original_height / 640)
#             x_max = int(x_max * original_width / 640)
#             y_max = int(y_max * original_height / 640)
#             parsed_boxes.append([x_min, y_min, x_max, y_max])
#             confidences.append(float(confidence))
#             class_ids.append(int(label))

 
#     # 박스 그리기
#     draw_boxes(frame, parsed_boxes, confidences, class_ids, classes)

#     # 특정 클래스(traffic_light) 색상 추출
#     for i, class_id in enumerate(class_ids):
#         if classes[class_id] == 'traffic_light':
#             colors = extract_color(frame, parsed_boxes[i])
#             print(f"Traffic light colors: {colors}")

#     # 결과 이미지 표시
#     cv2.imshow("Detection Results", frame)
    
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # 웹캠 릴리즈 및 윈도우 닫기
# cap.release()
# cv2.destroyAllWindows()
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

def histogram_stretching(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate histogram
    hist, bins = np.histogram(gray.flatten(), 256, [0,256])
    
    # Calculate cumulative distribution function
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max() / cdf.max()
    
    # Perform histogram stretching
    min_cdf = cdf.min()
    max_cdf = cdf.max()
    stretched = (cdf_normalized[gray] - min_cdf) * 255 / (max_cdf - min_cdf)
    stretched[stretched < 0] = 0
    stretched[stretched > 255] = 255
    stretched = stretched.astype('uint8')
    
    return stretched

# COCO 클래스 이름 로드
classes = ['left_traffic_sign', 'traffic_light']

# 모델과 가중치 파일 경로
model_xml = "model/model.xml"
model_bin = "model/model.bin"

# OpenVINO Inference Engine 초기화
ie = Core()

# 모델 로드 및 컴파일
model = ie.read_model(model=model_xml, weights=model_bin)
compiled_model = ie.compile_model(model=model, device_name="CPU")

# 웹캠 초기화
cap = cv2.VideoCapture("MAN_20240621_185159_F.MP4")  # Using webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    original_height, original_width = frame.shape[:2]

    # 히스토그램 스트레칭 적용
    frame_stretched = histogram_stretching(frame)

    # 히스토그램 스트레칭된 이미지를 CHW 순서로 변환
    frame_stretched_chw = frame_stretched.transpose((2, 0, 1))

    # 추론 실행을 위해 원본 크기로 변환하지 않고 그대로 사용
    input_data = np.expand_dims(frame_stretched_chw, axis=0).astype(np.float32)

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
        if confidence > 0.5:  # 신뢰도가 0.5보다 큰 경우만 고려
            x_min = int(x_min * original_width / 640)
            y_min = int(y_min * original_height / 640)
            x_max = int(x_max * original_width / 640)
            y_max = int(y_max * original_height / 640)
            parsed_boxes.append([x_min, y_min, x_max, y_max])
            confidences.append(float(confidence))
            class_ids.append(int(label))

    # 박스 그리기
    draw_boxes(frame, parsed_boxes, confidences, class_ids, classes)

    # 결과 이미지 표시
    cv2.imshow("Detection Results", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 웹캠 릴리즈 및 윈도우 닫기
cap.release()
cv2.destroyAllWindows()
