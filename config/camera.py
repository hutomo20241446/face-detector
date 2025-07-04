"""config/camera.py"""

import cv2
import time
os.environ['TZ'] = 'Asia/Jakarta'
time.tzset()

from urllib.parse import urlparse
from utils.retry import retry
from config.settings import Settings

settings = Settings()

class CameraConfig:
    def __init__(self):
        self.stream_url = settings.CAMERA_URL
        self.timeout = settings.CAMERA_TIMEOUT
        self.retry_interval = settings.CAMERA_RETRY_INTERVAL
        self.cap = None

    @retry(max_retries=5, delay=2, backoff=2)
    def connect(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
            
        self.cap = cv2.VideoCapture(self.stream_url)
        if not self.cap.isOpened():
            raise ConnectionError(f"Failed to connect to camera at {self.stream_url}")
        return self.cap

    def read_frame(self):
        if not self.cap or not self.cap.isOpened():
            self.connect()
            
        ret, frame = self.cap.read()
        if not ret:
            raise ConnectionError("Failed to read frame from camera")
        return frame

    def release(self):
        if self.cap:
            self.cap.release()
            