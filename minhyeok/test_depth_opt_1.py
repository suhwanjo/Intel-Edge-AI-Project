import time
from pathlib import Path
import cv2
import numpy as np
import openvino as ov
from openvino.inference_engine import IECore
import ipywidgets as widgets
import matplotlib.cm

class BoundingBox:
    """ 이 클래스를 통해 가장 가까운 차량의 정보를 저장 또는 업데이트 할 수 있음 """
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin, self.ymin, self.xmax, self.ymax = xmin, ymin, xmax, ymax
        self.miss_cnt = 0
        self.max_value = 0

    """ 불필요한 값이 측정될 경우에 카운트를 하는 함수 """
    def miss_count(self):
        self.miss_cnt += 1

""" 바운딩 박스 객체 정보 업데이트 """
def update_bounding_box(bounding_box, xmin, ymin, xmax, ymax):
    bounding_box.xmin, bounding_box.ymin, bounding_box.xmax, bounding_box.ymax = xmin, ymin, xmax, ymax

""" 이미지 정규화 """
def normalize_minmax(data):
    return (data - data.min()) / (data.max() - data.min())

""" 입력된 이미지 데이터를 입력된 컬러맵을 사용하여 색상화 """
def convert_result_to_image(result, colormap="viridis"):
    normalized_result = normalize_minmax(result.squeeze(0))
    colored_result = matplotlib.cm.get_cmap(colormap)(normalized_result)[:, :, :3] * 255
    return colored_result.astype(np.uint8)

""" BGQ -> RGB """
def to_rgb(image_data):
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

# 모델 경로 설정
model_depth_xml_path = "/home/ubuntu/intel_project_left_sign/otx/model/MiDaS_small.xml"
model_detection_xml_path = "/home/ubuntu/intel_project_left_sign/otx/model/vehicle-detection-adas-0002.xml"

# 캐시화 폴더 생성 -> 불필요한 움직임을 최소화하기 위함
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

# 비디오 설정
cap = cv2.VideoCapture("/home/ubuntu/intel_project_left_sign/otx/data/test_video.MP4")

while cap.isOpened():
    
    ret, frame = cap.read()
    if not ret:
        break
    
    # 특정 영역 crop
    cropped_frame = frame[:, :int(frame.shape[1]*0.53)]  
    
    # 모델 대입
    resized_image_detection = cv2.resize(src=cropped_frame, dsize=(network_image_width_detection, network_image_height_detection))
    input_image_detection = np.expand_dims(np.transpose(resized_image_detection, (2, 0, 1)), 0)
    result_detection = compiled_model_detection([input_image_detection])[output_key_detection]
    
    # 감지된 차량 영역의 중심점 초기화
    center_x, center_y = 0, 0
    max_y = 0

    for index, detection in enumerate(result_detection[0][0]):
        confidence = detection[2]
        if confidence > 0.5:  
            xmin = int(detection[3] * cropped_frame.shape[1])
            ymin = int(detection[4] * cropped_frame.shape[0])
            xmax = int(detection[5] * cropped_frame.shape[1])
            ymax = int(detection[6] * cropped_frame.shape[0])
            
            if max_y < ymax: # 최대 y값을 찾고 저장
                max_y = ymax
                if bounding_box is None:
                    bounding_box = BoundingBox(xmin, ymin, xmax, ymax)
                else:
                    if bounding_box.ymax > max_y:
                        bounding_box.miss_count()
                    else:
                        update_bounding_box(bounding_box, xmin, ymin, xmax, ymax)
                        bounding_box.miss_cnt = 0
    
    # 미스 카운트 10 초과 시, 객체 초기화
    if bounding_box.miss_cnt > 10: 
        update_bounding_box(bounding_box, 0, 0, 0, 0)
        bounding_box.miss_cnt = 0
    else:
        center_x = (bounding_box.xmin + bounding_box.xmax) // 2
        center_y = (bounding_box.ymin + bounding_box.ymax) // 2
        cv2.rectangle(frame, (bounding_box.xmin, bounding_box.ymin), (bounding_box.xmax, bounding_box.ymax), (0, 255, 0), 2)

        # 중심점 좌표를 이용하여 깊이(거리) 추정
        resized_image_depth = cv2.resize(src=frame, dsize=(network_image_width_depth, network_image_height_depth))
        input_image_depth = np.expand_dims(np.transpose(resized_image_depth, (2, 0, 1)), 0)
        result_depth = compiled_model_depth([input_image_depth])[output_key_depth]
        
        result_depth_rescaled = cv2.resize(result_depth[0], (frame.shape[1], frame.shape[0]))
        
        depth_value = result_depth_rescaled[center_y, center_x]
        cv2.putText(frame, f'Distance: {depth_value:.2f}', (bounding_box.xmin, bounding_box.ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        print(f"Detected vehicle depth at center: {depth_value}")
    
    # 아래에 가까운 차량 거리를 통한 처리 코드 작성
    if depth_value > 400.0:
        cv2.putText(frame, 'Danger!!', (frame.shape[1] // 4, frame.shape[0] // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    cv2.imshow('Object Detection and Depth Estimation', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()