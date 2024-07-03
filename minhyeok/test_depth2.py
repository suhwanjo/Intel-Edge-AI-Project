import time
from pathlib import Path

import cv2
import matplotlib.cm
import numpy as np
import openvino as ov
import ipywidgets as widgets

start_time = time.time()

class BoundingBox:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.miss_cnt = 0  # 최대 바운딩 박스 객체를 인식하지 못한 경우의 수를 카운트하는 변수
        self.max_value = 0

    def miss_count(self):
        self.miss_cnt += 1

def update_bounding_box(bounding_box, xmin, ymin, xmax, ymax):
    bounding_box.xmin = xmin
    bounding_box.ymin = ymin
    bounding_box.xmax = xmax
    bounding_box.ymax = ymax

def normalize_minmax(data):
    """Normalizes the values in `data` between 0 and 1"""
    return (data - data.min()) / (data.max() - data.min())

def convert_result_to_image(result, colormap="viridis"):
    "asd"
    cmap = matplotlib.cm.get_cmap(colormap)
    result = result.squeeze(0)
    result = normalize_minmax(result)
    result = cmap(result)[:, :, :3] * 255
    result = result.astype(np.uint8)
    return result

def to_rgb(image_data) -> np.ndarray:
    """Convert image_data from BGR to RGB"""
    return cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)

# OpenVINO Core 초기화 및 모델 컴파일
core = ov.Core()
device = widgets.Dropdown(
    options=core.available_devices + ["AUTO"],
    value="AUTO",
    description="Device:",
    disabled=False,
)

# 가장 가까운 객체 검출용 객체 생성
bounding_box = None

model_depth_xml_path = "/home/ubuntu/intel_project_left_sign/otx/model/MiDaS_small.xml"
model_detection_xml_path = "/home/ubuntu/intel_project_left_sign/otx/model/vehicle-detection-adas-0002.xml"

# Create cache folder
# "성능을 높이 위해서(불필요한 움직임 최소화)"
cache_folder = Path("cache")
cache_folder.mkdir(exist_ok=True)

core.set_property({"CACHE_DIR": cache_folder})

# 깊이 맵 모델 컴파일
model_depth = core.read_model(model_depth_xml_path)
compiled_model_depth = core.compile_model(model=model_depth, device_name=device.value)

input_key_depth = compiled_model_depth.input(0)
output_key_depth = compiled_model_depth.output(0)

# 깊이 추정 모델이 필요로하는 데이터 사이즈 추출
network_input_shape_depth = list(input_key_depth.shape)
network_image_height_depth, network_image_width_depth = network_input_shape_depth[2:]

# 차량 감지 모델 컴파일
model_detection = core.read_model(model_detection_xml_path)
compiled_model_detection = core.compile_model(model=model_detection, device_name=device.value)

input_key_detection = compiled_model_detection.input(0)
output_key_detection = compiled_model_detection.output(0)

# 차량 인식 모델이 필요로하는 데이터 사이즈 추출
network_input_shape_detection = list(input_key_detection.shape)
network_image_height_detection, network_image_width_detection = network_input_shape_detection[2:]

# 실시간 웹캠 피드와 거리 측정 및 차량 감지
# cap = cv2.VideoCapture("/home/ubuntu/Videos/Screencasts/ch4.webm")
cap = cv2.VideoCapture("/home/ubuntu/intel_project_left_sign/otx/data/test_video.MP4")

paused = False
paused_frame = None
alarm_triggered = False  # 경고음을 재생했는지 추적하는 변수
frame_count = 0
consecutive_depth_count = 0  # 연속된 깊이 값이 200을 초과하는 경우의 횟수를 추적하는 변수

while cap.isOpened():
    
    if not paused:
        ret, frame = cap.read()
        if not ret:
            break
        # 차량 감지
        cropped_frame = frame[:, :int(frame.shape[1]*0.6)]  # 특정 영역 crop
        
        resized_image_detection = cv2.resize(src=cropped_frame, dsize=(network_image_width_detection, network_image_height_detection))
        input_image_detection = np.expand_dims(np.transpose(resized_image_detection, (2, 0, 1)), 0)
        result_detection = compiled_model_detection([input_image_detection])[output_key_detection]
        
        # 감지된 차량 영역의 중심점 초기화
        center_x = 0
        center_y = 0
        
        max_y = 0  # 가장 높은 y축 값

        last_detection_index = len(result_detection[0][0]) - 1

        for index, detection in enumerate(result_detection[0][0]):
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
                        if(bounding_box.ymax > max_y):
                            bounding_box.miss_count()
                            # cv2.addWeighted(frame, )
                            # cv2.rectangle(frame, (0, 0), (0, 0), (0, 255, 0), 2)
                            # cv2.rectangle(frame, (bounding_box.xmin, bounding_box.ymin), (bounding_box.xmax, bounding_box.ymax), (0, 0, 0), -1)
                        else:
                            update_bounding_box(bounding_box, xmin, ymin, xmax, ymax)
                            bounding_box.miss_cnt = 0
        
        if(bounding_box.miss_cnt > 10):
            print("***************")
            print("***************")
            update_bounding_box(bounding_box, 0, 0, 0, 0)
        else:
            center_x = (bounding_box.xmin + bounding_box.xmax) // 2
            center_y = (bounding_box.ymin + bounding_box.ymax) // 2
            cv2.rectangle(frame, (bounding_box.xmin, bounding_box.ymin), (bounding_box.xmax, bounding_box.ymax), (0, 255, 0), 2)

            # 중심점 좌표를 이용하여 깊이(거리) 추정
            resized_image_depth = cv2.resize(src=frame, dsize=(network_image_width_depth, network_image_height_depth))
            input_image_depth = np.expand_dims(np.transpose(resized_image_depth, (2, 0, 1)), 0)
            result_depth = compiled_model_depth([input_image_depth])[output_key_depth]
            
            result_depth_rescaled = cv2.resize(result_depth[0], (frame.shape[1], frame.shape[0]))
            
            depth_value = result_depth_rescaled[center_y, center_x]  # 수정된 부분
            cv2.putText(frame, f'Distance: {depth_value:.2f}', (bounding_box.xmin, bounding_box.ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            print(f"Detected vehicle depth at center: {depth_value}")
            # depth_values.append(depth_value)  # 깊이 값을 리스트에 추가

        
        # 아래에 가까운 차량 거리를 통한 처리 코드 작성
        if depth_value > 200.0:
            print("************")
            cv2.putText(frame, 'Danger!!', (frame.shape[1] // 4, frame.shape[0] // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # 프레임을 일시정지 상태에서 사용할 수 있도록 저장
        paused_frame = frame.copy()
        
    else:
        # 일시정지 상태에서는 저장된 프레임을 표시
        if paused_frame is not None:
            frame = paused_frame
    
    # combined_image = np.hstack((frame, result_image))
    cv2.imshow('Object Detection and Depth Estimation', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('p'):
        paused = not paused
        if paused:
            print("Paused")
        else:
            print("Resumed")

cap.release()
cv2.destroyAllWindows()

end_time = time.time()
execution_time = end_time - start_time
print(f"코드 실행이 완료되었습니다. 총 소요된 시간: {execution_time} 초")

# 코드 실행이 완료되었습니다. 총 소요된 시간: 17.79334783554077 초
# 코드 실행이 완료되었습니다. 총 소요된 시간: 85.18706560134888 초