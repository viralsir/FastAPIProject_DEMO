from pydantic import BaseModel, Field


class StudentBase(BaseModel):
   rollno:int=Field(...,description="roll no")
   name:str=Field(...,description="student name",max_length=50)
   age:int=Field(...,description="student age",gt=0)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
     pass

class StudentResponse(StudentBase):
    rollno:int
    name:str

    model_config = {"from_attributes":True}



