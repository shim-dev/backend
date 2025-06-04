from flask import Blueprint, request, jsonify
import numpy as np
import cv2
from ultralytics import YOLO

yolo_bp = Blueprint('yolo', __name__)


# 음식 인식 코드
model = YOLO("C:\\Users\\Admin\\Desktop\\train12\\weights\\best.pt")  # 커스텀 음식 모델이 있다면 여기서 교체
@yolo_bp.route('/detect', methods=['POST'])
def detect_food():
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    results = model(img)[0]

    response = []
    for box in results.boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        conf = float(box.conf[0])
        response.append({
            'label': label,
            'confidence': round(conf, 2)
        })

    return jsonify(response)