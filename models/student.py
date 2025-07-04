"""model/student.py"""

from sqlalchemy import Column, String
from config.database import Base

class Student:
    def __init__(self, student_id, name, photo_url):
        self.student_id = student_id
        self.name = name
        self.photo_url = photo_url

# Model SQLAlchemy terpisah
class StudentDB(Base):
    __tablename__ = 'Students'

    student_id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    photo = Column(String(255))

    def __repr__(self):
        return f"<StudentDB(id={self.student_id}, name={self.name})>"