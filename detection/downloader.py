"""detection/downloader.py"""

import os
import numpy as np
import cv2
import requests
import logging
from sqlalchemy import text
from config.database import DatabaseConfig
from config.settings import Settings
from models.student import Student
from utils.retry import retry

# Initialize settings and database
settings = Settings()
db_config = DatabaseConfig()

class PhotoDownloader:
    def __init__(self):
        """Initialize the downloader with SIFT detector and required directories"""
        self.sift = cv2.SIFT_create()
        self._ensure_directories()
        self.processed_files = set()
        self._load_existing_features()
        
        # Configure logging
        self.logger = logging.getLogger('face_detection.downloader')
        self.logger.setLevel(settings.LOG_LEVEL)

    def _ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(settings.FEATURES_DIR, exist_ok=True)
        os.makedirs(settings.PHOTO_DIR, exist_ok=True)
        
        # Debugging: Print the paths to verify
        print(f"FEATURES_DIR: {settings.FEATURES_DIR}")
        print(f"PHOTO_DIR: {settings.PHOTO_DIR}")

    def _load_existing_features(self):
        """Load already processed files to avoid re-processing"""
        if os.path.exists(settings.FEATURES_DIR):
            self.processed_files = {
                f.split('.')[0] for f in os.listdir(settings.FEATURES_DIR) 
                if f.endswith('.npy')
            }

    @retry(max_retries=3, delay=1, backoff=2)
    def get_students_with_photos(self):
        """
        Retrieve students with photos from database
        Returns:
            List[Student]: List of Student objects
        """
        students = []
        try:
            with db_config.get_session() as session:
                query = text("""
                    SELECT DISTINCT s.student_id, s.name, s.photo as photo_url
                    FROM Students s
                    JOIN CourseEnrollments ce ON s.student_id = ce.student_id
                    JOIN Courses c ON ce.course_id = c.course_id
                    WHERE c.course_name IN :courses
                    AND s.photo IS NOT NULL
                """)
                
                # Eksekusi query dengan parameter yang benar
                result = session.execute(
                    query, 
                    {'courses': tuple(settings.TARGET_COURSES)}
                )
                
                # Konversi ke dictionary jika perlu
                if hasattr(result, 'mappings'):
                    rows = result.mappings().all()
                    for row in rows:
                        student = Student(
                            student_id=row['student_id'],
                            name=row['name'],
                            photo_url=row['photo_url']
                        )
                        students.append(student)
                else:
                    # Fallback untuk versi SQLAlchemy yang lebih lama
                    for row in result:
                        student = Student(
                            student_id=row[0],  # student_id
                            name=row[1],       # name
                            photo_url=row[2]    # photo_url
                        )
                        students.append(student)
                        
                self.logger.info(f"Retrieved {len(students)} students from database")
                return students
                
        except Exception as e:
            self.logger.error(f"Failed to fetch students from database: {str(e)}")
            raise

    @retry(max_retries=3, delay=2, backoff=2)
    def _download_photo(self, student):
        """
        Download individual student photo
        Args:
            student (Student): Student object containing photo_url
        Returns:
            np.ndarray: Downloaded image in grayscale
        """
        try:
            response = requests.get(
                student.photo_url,
                timeout=10,
                headers={'User-Agent': 'FaceDetectionApp/1.0'}
            )
            response.raise_for_status()
            
            img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
            
            if img is None:
                raise ValueError("Failed to decode image")
                
            return img
            
        except Exception as e:
            self.logger.error(f"Failed to download photo for {student.student_id}: {str(e)}")
            raise

    def _extract_features(self, image):
        """
        Extract SIFT features from an image
        Args:
            image (np.ndarray): Grayscale image
        Returns:
            tuple: (keypoints, descriptors) or (None, None) if extraction fails
        """
        try:
            keypoints, descriptors = self.sift.detectAndCompute(image, None)
            if descriptors is None or len(descriptors) < 10:
                raise ValueError("Not enough features detected")
            return keypoints, descriptors
        except Exception as e:
            self.logger.warning(f"Feature extraction failed: {str(e)}")
            return None, None

    def _save_features(self, student_id, descriptors):
        """
        Save SIFT descriptors to disk
        Args:
            student_id (str): Student ID
            descriptors (np.ndarray): SIFT descriptors
        """
        try:
            feature_path = os.path.join(settings.FEATURES_DIR, f"{student_id}.npy")
            np.save(feature_path, descriptors)
            self.processed_files.add(student_id)
        except Exception as e:
            self.logger.error(f"Failed to save features for {student_id}: {str(e)}")
            raise

    def process_student(self, student):
        """
        Process a single student: download photo and extract features
        Args:
            student (Student): Student to process
        Returns:
            bool: True if successful, False otherwise
        """
        if student.student_id in self.processed_files:
            self.logger.debug(f"Skipping already processed student: {student.student_id}")
            return True
            
        try:
            # Step 1: Download photo
            self.logger.info(f"Processing student: {student.student_id}")
            img = self._download_photo(student)
            
            # Step 2: Extract features
            _, descriptors = self._extract_features(img)
            if descriptors is None:
                return False
                
            # Step 3: Save features
            self._save_features(student.student_id, descriptors)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to process student {student.student_id}: {str(e)}")
            return False

    def run(self):
        """
        Main method to run the download and feature extraction process
        """
        try:
            self.logger.info("Starting photo download and feature extraction")
            
            # Get students from database
            students = self.get_students_with_photos()
            total_students = len(students)
            success_count = 0
            
            if not students:
                self.logger.warning("No students found with photos")
                return
            
            # Process each student
            for i, student in enumerate(students, 1):
                try:
                    if self.process_student(student):
                        success_count += 1
                    
                    # Log progress
                    if i % 10 == 0 or i == total_students:
                        progress = (i / total_students) * 100
                        self.logger.info(
                            f"Progress: {i}/{total_students} ({progress:.1f}%) | "
                            f"Success: {success_count} | Failed: {i - success_count}"
                        )
                        
                except Exception as e:
                    self.logger.error(f"Error processing student {student.student_id}: {str(e)}")
                    continue
            
            self.logger.info(
                f"Process completed. Success: {success_count}/{total_students} "
                f"({success_count/total_students*100:.1f}%)"
            )
            
        except Exception as e:
            self.logger.error(f"Fatal error in downloader: {str(e)}", exc_info=True)
            raise