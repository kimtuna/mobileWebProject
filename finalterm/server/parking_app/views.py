from django.shortcuts import render
from django.http import JsonResponse
import subprocess
import json

def detect_cars(request):
    # YOLOv5 실행 및 결과 얻기
    yolo_result = subprocess.run(["python", "path_to_yolov5/detect.py", "--source", "path_to_your_image_or_video"], capture_output=True)
    car_count = len(json.loads(yolo_result.stdout)["results"])

    # 감지된 차량 수를 모델에 저장하거나 다른 작업 수행
    # 예시: Car.objects.create(car_count=car_count)

    return JsonResponse({"car_count": car_count})
