# Main FastAPI application
# --------------------------------------

# Imports
# --------------------------------------
from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name": "John",
        "age": 17,
        "class": "year 12",
    },
    2: {
        "name": "Jane",
        "age": 16,
        "class": "year 11"
    },
    3: {
        "name": "Bob",
        "age": 18,
        "class": "year 13"
    },
}

class Student(BaseModel):
    name: str
    age: int
    class_: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    class_: Optional[str] = None

# Routes
# --------------------------------------
@app.get("/")
def index():
    return {"data": "Hello World"}

@app.get("/students")
def get_students():
    return students

@app.get("/students/{student_id}")
def get_student(student_id: int = Path(description="The ID of the student you want to view", gt=0, lt=4)):
    return students[student_id]

@app.get("/get-by-name")
def get_student_by_name(name: Optional[str] = None):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"data": "Student not found"}

@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student ID already exists"}
    students[student_id] = student
    return students[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student ID does not exist"}

    if student.name != None:
        students[student_id].name = student.name
    if student.age != None:
        students[student_id].age = student.age
    if student.class_ != None:
        students[student_id].class_ = student.class_

    return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student ID does not exist"}
    del students[student_id]
    return {"Message": "Student deleted successfully"}