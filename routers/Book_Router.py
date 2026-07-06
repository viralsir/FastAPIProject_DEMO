from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status
from sqlalchemy import select

from database import get_db
from model import Author, Book
from schemas.book_schema import BookResponse

#http://localhost/books
bookrouter = APIRouter(prefix="/book",tags=["Book"])

#create a new book
@bookrouter.post("/")
async def create_book(book:dict,db:AsyncSession=Depends(get_db)):
    new_book=Book(**book)
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book


#get all the books
@bookrouter.get("/",response_model=list[BookResponse],status_code=status.HTTP_200_OK)
async def get_all_books(db:AsyncSession=Depends(get_db)):
    result =  await db.execute(select(Book).options(selectinload(Book.authorinfo)))
    bookslist=result.scalars().all()
    return bookslist

# get book by id
@bookrouter.get("/{id}",response_model=BookResponse,status_code=status.HTTP_200_OK)
async def get_book_by_id(id:int,db:AsyncSession=Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == id))
    book = result.scalars().first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")
    return book

# update book detail by id
@bookrouter.put("/{id}",response_model=BookResponse)
async def update_book(id:int,book:dict,db:AsyncSession=Depends(get_db)):
    sbook = db.get(Book,id)
    if sbook is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")
    sbook=Book(**book)
    await db.merge(sbook)
    await db.commit()

    return sbook


#delete the book by id
@bookrouter.delete("/{id}",status_code=status.HTTP_200_OK)
async def delete_book(id:int,db:AsyncSession=Depends(get_db)):
    sbook = db.get(Book,id)
    if sbook is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")
    await db.delete(sbook)
    await db.commit()
    return {"message":"Book deleted successfully"}


