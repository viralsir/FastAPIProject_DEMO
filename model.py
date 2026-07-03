from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class student(Base):
    __tablename__ = "studentinfo"

    rollno:Mapped[int] = mapped_column(Integer,primary_key=True)
    name:Mapped[str] = mapped_column(String(255))
    fees:Mapped[int] = mapped_column(Integer)
    
