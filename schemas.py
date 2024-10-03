# backend/schemas.py

from pydantic import BaseModel



class LectureCreate(BaseModel):
    name: str

class LectureResponse(BaseModel):
    id: int
    name: str

class LectureListResponse(BaseModel):
    message: str
    lectures: list[LectureResponse]

class StudentCreate(BaseModel):
    name: str

class StudentResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True  # Позволяет работать с ORM объектами

class StudentAttendance(BaseModel):
    id: int
    name: str
    present: bool

class AttendanceCreate(BaseModel):
    lecture_id: int
    date: str  # You may want to use `datetime` depending on your needs
    students: list[StudentAttendance]


class AttendanceResponse(BaseModel):
    id: int
    student: StudentResponse  # Связь с студентом
    lecture: LectureResponse  # Связь с лекцией
    date: str
    present: int
    
    class Config:
        orm_mode = True

class GoodResponse(BaseModel):
    message: str
    
#class AttendanceResponse(BaseModel):
#    message: str
#    data: list[AttendanceCreate]
#
#    class Config:
#        orm_mode = True