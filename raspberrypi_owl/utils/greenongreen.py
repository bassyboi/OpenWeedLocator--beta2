#!/usr/bin/env python
import cv2
from pathlib import Path

# Hypothetical Hailo SDK imports - adjust with actual import statements from Hailo SDK
from hailo_platform import HailoModel, HailoSDK  # Replace with the correct imports from Hailo SDK

# PyCoral imports for Coral Edge TPU - adjust as necessary
from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference

class GreenOnGreen:
    def __init__(self, model_type='hailo', model_path=None, label_file=None):
        """
        Initialize the GreenOnGreen class for Hailo or Coral Edge TPU inference.

        Args:
            model_type (str): Specify 'hailo' for Hailo-8 AI module or 'coral' for Coral Edge TPU.
            model_path (str): Path to the model file.
            label_file (str): Path to the labels file.
        """
        self.model_type = model_type.lower()
        self.model_path = Path(model_path)
        self.label_file = Path(label_file)

        # Initialize based on model type
        if self.model_type == 'hailo':
            self.init_hailo_model()
        elif self.model_type == 'coral':
            self.init_coral_model()
        else:
            raise ValueError("Invalid model_type. Use 'hailo' or 'coral'.")

        self.labels = self.read_label_file(self.label_file)

    def read_label_file(self, label_file):
        # Read the labels file
        with open(label_file, 'r') as file:
            labels = file.read().splitlines()
        return {idx: label for idx, label in enumerate(labels)}

    def init_hailo_model(self):
        """
        Initialize Hailo-8 AI model using Hailo SDK.
        """
        # Initialize Hailo model
        self.model_path = self.model_path.with_suffix('.hailomodel')  # Ensure the correct file extension
        self.model = HailoModel(self.model_path.as_posix())  # Adjust with actual Hailo API calls
        self.sdk = HailoSDK()  # Hypothetical SDK initializer, replace with actual API
        self.sdk.allocate_model(self.model)
        
        # Get input size from Hailo model
        self.inference_size = self.model.input_size()
        print(f'[INFO] Initialized Hailo-8 model: {self.model_path.stem}.')

    def init_coral_model(self):
        """
        Initialize Coral Edge TPU model.
        """
        self.model_path = self.model_path.with_suffix('.tflite')  # Ensure the correct file extension

        if not self.model_path.exists():
            raise FileNotFoundError(f'Coral model file not found at {self.model_path.as_posix()}')

        # Initialize Coral Edge TPU interpreter
        self.interpreter = make_interpreter(self.model_path.as_posix())
        self.interpreter.allocate_tensors()
        self.inference_size = input_size(self.interpreter)
        print(f'[INFO] Initialized Coral Edge TPU model: {self.model_path.stem}.')

    def inference(self, image, confidence=0.5, filter_id=0):
        """
        Run inference using either Hailo-8 AI module or Coral Edge TPU.

        Args:
            image: Input image for inference.
            confidence: Confidence threshold for filtering detections.
            filter_id: Class ID to filter specific detections.

        Returns:
            Annotated image with bounding boxes and labels.
        """
        if self.model_type == 'hailo':
            return self.inference_hailo(image, confidence, filter_id)
        elif self.model_type == 'coral':
            return self.inference_coral(image, confidence, filter_id)

    def inference_hailo(self, image, confidence=0.5, filter_id=0):
        """
        Perform inference using Hailo-8 AI module.
        """
        # Preprocess the image as required by Hailo model
        cv2_im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2_im_rgb = cv2.resize(cv2_im_rgb, self.inference_size)
        
        # Run inference using Hailo SDK
        result = self.sdk.infer(cv2_im_rgb.tobytes())
        
        # Process the results (example, adjust to match actual output format)
        detections = self.process_hailo_detections(result, confidence, filter_id)
        weed_centers = []
        boxes = []

        for det in detections:
            x1, y1, x2, y2, conf, cls_id = det
            if cls_id == filter_id or filter_id == 0:
                label = f"{self.labels.get(cls_id, cls_id)}: {conf:.2f}"
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                # Compute center
                centerX = int(x1 + (x2 - x1) / 2)
                centerY = int(y1 + (y2 - y1) / 2)
                weed_centers.append([centerX, centerY])
                boxes.append([x1, y1, x2 - x1, y2 - y1])

        return None, boxes, weed_centers, image

    def inference_coral(self, image, confidence=0.5, filter_id=0):
        """
        Perform inference using Coral Edge TPU model.
        """
        cv2_im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2_im_rgb = cv2.resize(cv2_im_rgb, self.inference_size)
        run_inference(self.interpreter, cv2_im_rgb.tobytes())
        objects = get_objects(self.interpreter, confidence)

        height, width, channels = image.shape
        scale_x, scale_y = width / self.inference_size[0], height / self.inference_size[1]
        weed_centers = []
        boxes = []

        for det_object in objects:
            if det_object.id == filter_id:
                bbox = det_object.bbox.scale(scale_x, scale_y)

                startX, startY = int(bbox.xmin), int(bbox.ymin)
                endX, endY = int(bbox.xmax), int(bbox.ymax)
                boxW = endX - startX
                boxH = endY - startY

                # Save the bounding box
                boxes.append([startX, startY, boxW, boxH])
                # Compute box center
                centerX = int(startX + (boxW / 2))
                centerY = int(startY + (boxH / 2))
                weed_centers.append([centerX, centerY])

                percent = int(100 * det_object.score)
                label = f'{percent}% {self.labels.get(det_object.id, det_object.id)}'
                cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
                cv2.putText(image, label, (startX, startY + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)

        return None, boxes, weed_centers, image

    def process_hailo_detections(self, result, confidence, filter_id):
        """
        Process Hailo detections and filter them based on confidence and class.

        Args:
            result: The output from Hailo inference.
            confidence: Confidence threshold for filtering.
            filter_id: Class ID to filter specific detections.

        Returns:
            Filtered list of detections.
        """
        detections = []
        # Assuming 'result' format from Hailo inference contains bounding boxes and confidence
        for det in result:
            x1, y1, x2, y2, conf, cls_id = det  # Adjust based on Hailo output structure
            if conf >= confidence and (filter_id == 0 or cls_id == filter_id):
                detections.append((x1, y1, x2, y2, conf, cls_id))
        return detections

# Usage Example
if __name__ == "__main__":
    # Initialize the GreenOnGreen object for Hailo-8 AI module
    hailo_detector = GreenOnGreen(
        model_type='hailo',
        model_path='/OpenWeedLocator/hailo_models/my_hailo_model',
        label_file='/OpenWeedLocator/hailo_models/labels.txt'
    )
    
    # Load input image for inference
    input_image = cv2.imread('/OpenWeedLocator/input_image.jpg')  # Adjust path to your input image
    _, boxes, weed_centers, output_image = hailo_detector.inference(input_image)
    
    # Display the output image
    cv2.imshow('Hailo Output', output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Initialize the GreenOnGreen object for Coral Edge TPU
    coral_detector = GreenOnGreen(
        model_type='coral',
        model_path='/OpenWeedLocator/coral_models/my_coral_model',
        label_file='/OpenWeedLocator/coral_models/labels.txt'
    )

    # Load input image for inference
    _, boxes, weed_centers, output_image = coral_detector.inference(input_image)

    # Display the output image
    cv2.imshow('Coral Output', output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
