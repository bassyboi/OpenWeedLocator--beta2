import cv2
from imutils.video import VideoStream

class CameraHandler:
    def __init__(self, resolution=(416, 320), exp_compensation=-2):
        self.resolution = resolution
        self.exp_compensation = exp_compensation
        self.stream = None

    def start_camera(self):
        self.stream = VideoStream(resolution=self.resolution).start()

    def read_frame(self):
        if self.stream is not None:
            return self.stream.read()
        else:
            raise Exception("Camera stream not started. Call start_camera() first.")

    def stop_camera(self):
        if self.stream is not None:
            self.stream.stop()
