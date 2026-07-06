from fastapi import FastAPI
from pydantic import BaseModel
from routers import Student_Router, Author_Router, Book_Router, User_Router

app = FastAPI(title="first api")

app.include_router(Student_Router.router)

app.include_router(Author_Router.author_router)
app.include_router(Book_Router.bookrouter)
app.include_router(User_Router.userRouter)

# http://localhost:8000/
# @app.get("/")
# async def root():
#     print("client request for the root path")
#     return {"message": "Hello World"}
#
#
#
#
# # http://localhost:8000/hello/
# @app.get("/hello/")
# async def say_hello():
#     return {"message": f"Hello "}
#
# @app.get("/aboutus/")
# async def say_aboutus():
#     return {"message": "About Us"}
#
# #http://localhost:8000/contact
# @app.get("/contact/")
# async def say_contact():
#     return {"message": "Contact Us"}
#
#
# # fatch data from path  : path variable
# @app.get(("/hello/{name}"))
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
#
# @app.get("/hello/{name}/{age}")
# async def say_hello_age(name: str, age: int):
#     return {"message": f"Hello {name} and you age is {age}"}
#
# @app.get("/student/")
# async def say_student(rollno:int,name:str,age:int):
#     return {"rollno":rollno,"name":name,"age":age}
#
#
# # request mapping /
# # class StudentCreate(BaseModel):
# #     rollno: int
# #     name: str
# #     age: int | None
#
# @app.get("/studentinfo/")
# async def say_student(student: StudentCreate):
#     #return {"rollno":student.rollno,"name":student.name,"age":student.age}
#     return {**student.model_dump()}




