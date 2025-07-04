"""config/settings.py"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        # Camera settings
        self.CAMERA_URL = os.getenv('CAMERA_URL')
        self.CAMERA_TIMEOUT = int(os.getenv('CAMERA_TIMEOUT', '10'))
        self.CAMERA_RETRY_INTERVAL = int(os.getenv('CAMERA_RETRY_INTERVAL', '5'))
        
        # Database settings
        self.DB_HOST = os.getenv('DB_HOST')
        self.DB_PORT = int(os.getenv('DB_PORT'))
        self.DB_USER = os.getenv('DB_USER')
        self.DB_PASS = os.getenv('DB_PASS')
        self.DB_NAME = os.getenv('DB_NAME')
        
        # Directory settings
        self.PHOTO_DIR = 'photos'  # Direktori untuk menyimpan foto asli
        self.FEATURES_DIR = 'detection/features'  # Direktori untuk menyimpan fitur SIFT
        self.LOG_DIR = 'logs'
        
        # Detection settings
        self.MIN_MATCH_COUNT = int(os.getenv('MIN_MATCH_COUNT', '10'))
        self.REQUIRED_DETECTION_DURATION = int(os.getenv('REQUIRED_DETECTION_DURATION', '3'))
        self.TARGET_COURSES = ['Struktur Data', 'Algoritma Lanjut', 'Sistem Operasi']
        self.LOG_FILE = os.path.join(self.LOG_DIR, 'detection.log')
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
        
        # Create required directories
        os.makedirs(self.PHOTO_DIR, exist_ok=True)
        os.makedirs(self.FEATURES_DIR, exist_ok=True)
        os.makedirs(self.LOG_DIR, exist_ok=True)