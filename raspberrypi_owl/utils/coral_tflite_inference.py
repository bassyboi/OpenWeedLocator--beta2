# coral_tflite_inference.py
import tflite_runtime.interpreter as tflite

class CoralTFLiteInference:
    def __init__(self, model_path, confidence_threshold=0.5):
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.interpreter = None
        self._load_model()

    def _load_model(self):
        # Load the TFLite model for Coral
        self.interpreter = tflite.Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()

    def run_inference(self, input_data):
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        self.interpreter.set_tensor(input_details[0]['index'], input_data)
        self.interpreter.invoke()

        output_data = self.interpreter.get_tensor(output_details[0]['index'])
        return output_data if output_data[0] > self.confidence_threshold else None
