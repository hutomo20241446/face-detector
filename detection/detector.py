"""detection/detector.py"""

import os
import time
os.environ['TZ'] = 'Asia/Jakarta'
time.tzset()

import logging
from config.settings import Settings
from services.attendance_service import AttendanceService
from utils.retry import retry

settings = Settings()
logger = logging.getLogger('face_detection.detector')

class FaceDetector:
    def __init__(self):
        self.attendance_service = AttendanceService()
        self.current_detection = None
        self.detection_start_time = None
        self.logged_faces = set()
        self.last_attendance_time = {}

    @retry(max_retries=3, delay=1)
    def process_frame(self, frame, matcher):
        try:
            detected_face, max_matches, good_matches = matcher.match_face(frame)
            
            if detected_face == self.current_detection and detected_face is not None:
                detection_duration = time.time() - self.detection_start_time
                
                if detection_duration >= settings.REQUIRED_DETECTION_DURATION:
                    self._log_detection(detected_face, max_matches)
                    
                    if detected_face not in self.logged_faces:
                        self._record_attendance(detected_face)
                        self.logged_faces.add(detected_face)
            else:
                self.current_detection = detected_face
                self.detection_start_time = time.time() if detected_face is not None else None
                
        except Exception as e:
            logger.error(f"Error processing frame: {e}")
            raise

    def _log_detection(self, detected_face, matches_count):
        log_message = f"Detected {detected_face} (Matches: {matches_count})"
        logger.info(log_message)

    def _record_attendance(self, student_id):
        now = time.time()
        # Prevent duplicate recording within 5 minutes
        if student_id in self.last_attendance_time and (now - self.last_attendance_time[student_id]) < 300:
            logger.info(f"Attendance for {student_id} already recorded recently. Skipping.")
            return
            
        try:
            date_str = time.strftime("%Y-%m-%d")
            success = self.attendance_service.record_attendance(student_id, date_str)
            if success:
                self.last_attendance_time[student_id] = now
        except Exception as e:
            logger.error(f"Failed to record attendance for {student_id}: {e}")