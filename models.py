# backend/models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    # Связь с моделью Attendance
    attendances = relationship("Attendance", back_populates="student")

class Lecture(Base):
    __tablename__ = "lectures"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    # Связь с моделью Attendance
    attendances = relationship("Attendance", back_populates="lecture")

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    lecture_id = Column(Integer, ForeignKey("lectures.id"))
    date = Column(String, index=True)
    
    
    present = Column(Integer)  # 1 - присутствует, 0 - отсутствует

    # Связь с моделью Student
    student = relationship(Student, back_populates="attendances")
    
    # Связь с моделью Lecture
    lecture = relationship(Lecture, back_populates="attendances")


