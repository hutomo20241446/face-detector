"""detection/matcher.py"""

import os
import numpy as np
import cv2
from config.settings import Settings
import logging

settings = Settings()

class FaceMatcher:
    def __init__(self):
        self.sift = cv2.SIFT_create()
        self.flann = self._init_flann()
        self.reference_features = self._load_reference_features()

    def _init_flann(self):
        index_params = dict(algorithm=1, trees=5)
        search_params = dict(checks=50)
        return cv2.FlannBasedMatcher(index_params, search_params)

    def _load_reference_features(self):
        features = {}
        for file in os.listdir(settings.FEATURES_DIR):
            if file.endswith('.npy'):
                student_id = os.path.splitext(file)[0]
                descriptors = np.load(os.path.join(settings.FEATURES_DIR, file))
                features[student_id] = descriptors
        return features

    def match_face(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, current_descriptors = self.sift.detectAndCompute(gray, None)
        
        if current_descriptors is None:
            return None, 0, []

        best_match = None
        max_matches = 0
        best_good_matches = []

        for student_id, ref_descriptors in self.reference_features.items():
            matches = self.flann.knnMatch(ref_descriptors, current_descriptors, k=2)
            
            # Lowe's ratio test
            good_matches = []
            for m, n in matches:
                if m.distance < 0.7 * n.distance:
                    good_matches.append(m)
            
            if len(good_matches) > max_matches:
                max_matches = len(good_matches)
                best_match = student_id
                best_good_matches = good_matches

        if max_matches >= settings.MIN_MATCH_COUNT:
            return best_match, max_matches, best_good_matches
        
        return None, 0, []
        