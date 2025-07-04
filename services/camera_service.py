"""services/camera_service.py"""

import cv2
import time
from utils.retry import retry
from config.settings import Settings

settings = Settings()

class CameraService:
    def __init__(self):
        self.cap = None
        self.connect()

    @retry(max_retries=5, delay=2, backoff=2)
    def connect(self):
        if self.cap:
            self.cap.release()
            
        self.cap = cv2.VideoCapture(settings.CAMERA_URL)
        if not self.cap.isOpened():
            raise ConnectionError(f"Failed to connect to camera at {settings.CAMERA_URL}")
        return self.cap

    def get_frame(self):
        try:
            if not self.cap or not self.cap.isOpened():
                self.connect()
                
            ret, frame = self.cap.read()
            if not ret:
                raise ConnectionError("Failed to read frame")
            return frame
        except Exception as e:
            self.connect()
            raise

    def release(self):
        if self.cap:
            self.cap.release()