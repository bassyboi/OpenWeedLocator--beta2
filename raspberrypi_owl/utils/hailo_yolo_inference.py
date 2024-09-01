# hailo_yolo_inference.py
from ultralytics import YOLO  # Assuming you use the Ultralytics library for YOLOv8

class HailoYOLOInference:
    def __init__(self, model_path, confidence_threshold=0.5):
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.model = None
        self._load_model()

    def _load_model(self):
        # Load the YOLOv8 model
        self.model = YOLO(self.model_path)

    def run_inference(self, image):
        # Run inference with YOLOv8
        results = self.model(image)
        # Process the results
        detections = results[0].boxes.xyxy  # Example: get bounding boxes
        confidences = results[0].boxes.conf
        filtered_detections = [
            (box, conf) for box, conf in zip(detections, confidences) if conf >= self.confidence_threshold
        ]
        return filtered_detections
