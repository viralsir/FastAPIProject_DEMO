from fastapi import APIRouter, HTTPException

from schemas.student_schema import StudentResponse, StudentCreate, StudentUpdate

router=APIRouter(prefix="/student",tags=["student"])

student_db:list[StudentResponse]=[
    {"rollno":1,"name":"Amit","age":34},
    {"rollno":2,"name":"Rajan","age":55}
]
next_rollno=3

#view
# http://localhost:8000/student/ - get
@router.get("/",response_model=list[StudentResponse],status_code=200)
async def list_student():
    global student_db
    return student_db

#search
# http://localhost:8000/student/1  - get
@router.get("/{rollno}",response_model=StudentResponse,status_code=200)
async def search_student(rollno:int):
     student = next((s for s in student_db if s["rollno"]==rollno), None)
     if student is None:
        raise HTTPException(status_code=404,detail="student not found")
     return student

#new
#http://locahost:8000/student - post
@router.post("/",response_model=StudentResponse,status_code=200)
async def create_student(new_student: StudentCreate):
    global next_rollno
    global student_db

    student_db.append({**new_student.model_dump()})
    next_rollno+=1
    return {**new_student.model_dump()};

#update
@router.put("/{rollno}",response_model=StudentResponse,status_code=200)
async def update_student(rollno:int,student: StudentUpdate):
    global student_db
    student_info= next((s for s in student_db if s["rollno"]==rollno), None)
    if student_info is None:
        raise HTTPException(status_code=404,detail="student not found")
    student_db[student_db.index(student_info)].update(student.model_dump())
    return student_db[student_db.index(student_info)];



#delete
# http://localhost:8000/student/2
@router.delete("/{rollno}",response_model=list[StudentResponse])
async def delete_student(rollno:int):
    global student_db
    original_len=len(student_db)
    student_db=[student for student in student_db if student["rollno"]!=rollno]
    if len(student_db)==original_len:
        raise HTTPException(status_code=404,detail="student not found")
    return student_db