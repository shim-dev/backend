from flask import Blueprint, request, jsonify
import numpy as np
import cv2
from ultralytics import YOLO
import os

yolo_bp = Blueprint('yolo', __name__)

# 상대 경로로 모델 로드
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', '..', 'weights', 'best.pt')
model = YOLO(MODEL_PATH)


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
