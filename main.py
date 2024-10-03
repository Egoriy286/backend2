# backend/main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, database, schemas
from sqlalchemy import asc, desc  # Импортируем функции для сортировки
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import joinedload

origins = ["*"]


# Создаем таблицы, если они еще не созданы
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependency для получения сессии базы данных
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Эндпоинт для получения списка лекций
@app.get("/lectures", response_model=schemas.LectureListResponse)
def get_lectures( db: Session = Depends(get_db)):
    lectures = db.query(models.Lecture).all()
    return {"message": "Список пар успешно получен", "lectures": lectures}

@app.post("/lectures", response_model=schemas.LectureResponse)
def create_lecture(lecture: schemas.LectureCreate, db: Session = Depends(get_db)):
    db_lecture = models.Lecture(name=lecture.name)
    db.add(db_lecture)
    db.commit()
    db.refresh(db_lecture)
    return db_lecture

# Удаление пары
@app.delete("/lectures/{lecture_id}", response_model=schemas.StudentResponse)
def delete_lecture(lecture_id: int, db: Session = Depends(get_db)):
    lecture = db.query(models.Lecture).filter(models.Lecture.id == lecture_id).first()
    if lecture is None:
        raise HTTPException(status_code=404, detail="Lecture not found")
    db.delete(lecture)
    db.commit()
    return lecture

# Получение списка студентов с сортировкой
@app.get("/students", response_model=list[schemas.StudentResponse])
def read_students(sort_by: str = "id", order: str = "asc", db: Session = Depends(get_db)):
    query = db.query(models.Student)

    # Сортировка
    if sort_by not in ["id", "name"]:
        raise HTTPException(status_code=400, detail="Invalid sort_by field")
    
    if order == "desc":
        query = query.order_by(desc(sort_by))
    else:
        query = query.order_by(asc(sort_by))

    students = query.all()
    return students

# Добавление нового студента
@app.post("/students", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(name=student.name)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# Удаление студента
@app.delete("/students/{student_id}", response_model=schemas.StudentResponse)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return student

@app.post("/attendance", response_model=schemas.GoodResponse)
def create_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):

    
    # Проверяем, существует ли лекция с указанным ID
    for student in attendance.students:
        db_attendance = models.Attendance(
            student_id=student.id,
            lecture_id=attendance.lecture_id,
            date=attendance.date,
            present=int(student.present)  # Приводим значение к типу int
        )

        db.add(db_attendance)
    
    db.commit()  # Коммитим все добавленные записи
   
    return {"message": "Посещаемость успешно сохранена"}

# Удаление записи о посещаемости
@app.delete("/attendance/{attendance_id}", response_model=schemas.GoodResponse)
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    attendance = db.query(models.Attendance).filter(models.Attendance.id == attendance_id).first()
    if attendance is None:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    db.delete(attendance)
    db.commit()
    return {"message": "успешно удалено"}


@app.get("/attendance", response_model=list[schemas.AttendanceResponse])
def get_attendance(db: Session = Depends(get_db)):
    
    attendances = (
        db.query(models.Attendance)
        .options(joinedload(models.Attendance.student), joinedload(models.Attendance.lecture))
        .all()
    )
    return attendances
