import os
import json
import tarfile
import shutil

# 신호등-도로표지판 인지 영상 폴더 경로
base_dir = "신호등-도로표지판 인지 영상(수도권)"

# Training 폴더 경로
training_dir = os.path.join(base_dir, "Training")

# 압축 해제할 폴더 경로
extract_dir = os.path.join(training_dir, "extracted")

# 압축 해제할 폴더 생성
os.makedirs(extract_dir, exist_ok=True)

# 라벨 폴더와 원천 폴더 경로
label_dir = os.path.join(extract_dir, "d_train_1920_1080_daylight_7")
source_dir = os.path.join(extract_dir, "[원천]d_train_1920_1080_daylight_7")

# tar 파일 경로
label_tar = os.path.join(training_dir, "[라벨]d_train_1920_1080_daylight_7.tar")
source_tar = os.path.join(training_dir, "[원천]d_train_1920_1080_daylight_7.tar")

# tar 파일 압축 해제
with tarfile.open(label_tar, "r") as tar:
    tar.extractall(extract_dir)

with tarfile.open(source_tar, "r") as tar:
    tar.extractall(source_dir)

# 저장할 폴더 경로
save_label_dir = os.path.join(training_dir, "data", "라벨")
save_source_dir = os.path.join(training_dir, "data", "원천")

# 저장할 폴더 생성
os.makedirs(save_label_dir, exist_ok=True)
os.makedirs(save_source_dir, exist_ok=True)

# 라벨 폴더의 모든 JSON 파일 확인
for filename in os.listdir(label_dir):
    if filename.endswith(".json"):
        json_path = os.path.join(label_dir, filename)
        with open(json_path, "r") as file:
            data = json.load(file)
            
            # annotation 확인
            for annotation in data["annotation"]:
                if annotation["class"] == "traffic_sign" and annotation["shape"] == "rectangle" and annotation["color"] == "blue":
                    # 조건에 맞는 파일 출력
                    print("비보호 좌회전 File:", filename)
                    print("---")
                    
                    # 조건에 맞는 라벨 파일 저장
                    label_file = os.path.join(label_dir, filename)
                    shutil.copy(label_file, save_label_dir)
                    
                    # 조건에 맞는 원천 파일 저장
                    source_file = os.path.join(source_dir, filename.split('.')[0])
                    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']  # 이미지 파일 확장자 목록
                    for ext in image_extensions:
                        source_file_with_ext = source_file + ext
                        if os.path.isfile(source_file_with_ext):
                            shutil.copy(source_file_with_ext, save_source_dir)
                            break
                    
                    break