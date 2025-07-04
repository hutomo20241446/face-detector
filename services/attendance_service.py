"""
services/attendance_service.py
"""

from sqlalchemy import text
from datetime import datetime
from config.database import DatabaseConfig
import logging
from utils.retry import retry

logger = logging.getLogger('face_detection.attendance')

class AttendanceService:
    def __init__(self):
        self.db_config = DatabaseConfig()

    @retry(max_retries=3, delay=1, backoff=2)
    def record_attendance(self, student_id, date_str):
        """
        Menyesuaikan timezone Asia/Jakarta (UTC+7) untuk pencocokan dan penyimpanan.
        """
        with self.db_config.get_session() as session:
            try:
                # 1. Ubah tanggal input (lokal) jadi UTC di dalam SQL
                session_query = text("""
                    SELECT cs.session_id
                    FROM Students s
                    JOIN CourseEnrollments ce ON s.student_id = ce.student_id
                    JOIN ClassSessions cs ON ce.course_id = cs.course_id 
                        AND ce.semester_id = cs.semester_id
                    WHERE s.student_id = :student_id 
                    AND DATE(CONVERT_TZ(cs.date, 'UTC', 'Asia/Jakarta')) = :local_date
                """)
                
                result = session.execute(session_query, {
                    'student_id': student_id,
                    'local_date': date_str
                }).fetchone()
                
                if not result:
                    logger.warning(f"No session found for {student_id} on {date_str}")
                    return False

                # 2. Gunakan waktu lokal saat insert, tetap simpan sebagai UTC
                insert_query = text("""
                    INSERT INTO Attendances (attendance_id, session_id, student_id, timestamp)
                    VALUES (UUID(), :session_id, :student_id, CONVERT_TZ(NOW(), 'UTC', 'Asia/Jakarta'))
                """)
                
                session.execute(insert_query, {
                    'session_id': result[0],
                    'student_id': student_id
                })
                
                logger.info(f"Attendance recorded for {student_id} at 'Asia/Jakarta' timestamp")
                return True
                
            except Exception as e:
                logger.error(f"Failed to record attendance: {str(e)}")
                session.rollback()
                raise
