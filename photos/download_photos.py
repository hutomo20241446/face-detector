"""
photo/download_photos.py
Script untuk mendownload foto mahasiswa dan mengekstrak fitur SIFT
"""

import logging
from detection.downloader import PhotoDownloader
from utils.logging import configure_logging

def main():
    configure_logging()
    logger = logging.getLogger('photo_downloader')
    
    try:
        logger.info("Starting photo download and feature extraction process")
        downloader = PhotoDownloader()
        
        # Step 1: Download photos and extract SIFT features
        downloader.run()
        
        logger.info("Photo download and feature extraction completed successfully")
    except Exception as e:
        logger.error(f"Failed to download photos: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()