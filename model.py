from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class student(Base):
    __tablename__ = "studentinfo"

    rollno:Mapped[int] = mapped_column(Integer,primary_key=True)
    name:Mapped[str] = mapped_column(String(255))
    fees:Mapped[int] = mapped_column(Integer)


class Author(Base):
    __tablename__ = "authors"

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    name:Mapped[str] = mapped_column(String(255))
    email:Mapped[str] = mapped_column(String(255))

    books:Mapped[list["Book"]] = relationship(back_populates="authorinfo")


class Book(Base):
    __tablename__ = "books"

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    title:Mapped[str] = mapped_column(String(255))
    price:Mapped[int] = mapped_column(Integer)
    author:Mapped[int] = mapped_column(ForeignKey("authors.id"))

    authorinfo:Mapped["Author"] = relationship(back_populates="books")







