from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.student_schema import StudentResponse, StudentCreate, StudentUpdate

router=APIRouter(prefix="/student",tags=["student"])

#  http://localhost:8000/student    -  get - view  , post  - save ,put - update  ,delete - delete

student_db:list[StudentResponse]=[
    {"rollno":1,"name":"Amit","age":34},
    {"rollno":2,"name":"Rajan","age":55}
]
next_rollno=3

#view
# http://localhost:8000/student/ - get
@router.get("/",response_model=list[StudentResponse],status_code=200)
async def list_student(db:AsyncSession=Depends(get_db)):
   from model import student
   result = await db.execute(select(student))
   studentlist=result.scalars().all()

   return studentlist

#search
# http://localhost:8000/student/1  - get
@router.get("/{rollno}",response_model=StudentResponse,status_code=200)
async def search_student(rollno:int, db:AsyncSession=Depends(get_db)):
     from model import student

     studentinfo = await db.get(student,rollno)
     if studentinfo is None:
        raise HTTPException(status_code=404,detail="student not found")
     return studentinfo

#new
#http://locahost:8000/student - post
@router.post("/",response_model=StudentResponse,status_code=200)
async def create_student(student_data: dict , db:AsyncSession=Depends(get_db)):
   from  model import student
   new_student=student(**student_data)
   db.add(new_student)
   await db.commit()
   await db.refresh(new_student)

   return new_student;

#update
@router.put("/{rollno}",response_model=StudentResponse,status_code=200)
async def update_student(rollno:int,student_updated: dict,db:AsyncSession=Depends(get_db)):
   from model import student

   studentin=await db.get(student,rollno)
   if studentin is None:
        raise HTTPException(status_code=404,detail="student not found")

   studenti=student(**student_updated)
   update_student=await db.merge(studenti)
   await db.commit()

   return update_student



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