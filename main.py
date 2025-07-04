"""main.py"""

import time
import os
os.environ['TZ'] = 'Asia/Jakarta'
time.tzset()

import logging
from config.settings import Settings
from detection.detector import FaceDetector
from detection.matcher import FaceMatcher
from services.camera_service import CameraService
from utils.logging import configure_logging

configure_logging()

def main():
    settings = Settings()
    detector = FaceDetector()
    matcher = FaceMatcher()
    camera = CameraService()

    logging.info("Starting face detection service (headless mode)")
    
    try:
        while True:
            try:
                frame = camera.get_frame()
                detector.process_frame(frame, matcher)
                
            except ConnectionError as e:
                logging.warning(f"Camera error: {str(e)}. Reconnecting...")
                time.sleep(settings.CAMERA_RETRY_INTERVAL)
                
    except KeyboardInterrupt:
        logging.info("Shutting down gracefully")
    finally:
        camera.release()

if __name__ == "__main__":
    main()