from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from model import Author
from schemas.book_schema import AuthorResponse

author_router = APIRouter(prefix="/author",tags=["Author"])

# http://localhost:8000/author
#create new author in the database using post method
@author_router.post("/",response_model=AuthorResponse)
async def new_author(author:dict, db:AsyncSession=Depends(get_db)):
    crate_author = Author(**author)
    db.add(crate_author)
    await db.commit()
    await db.refresh(crate_author)
    return crate_author

# get all the Authors
@author_router.get("/",response_model=list[AuthorResponse])
async def get_authors(db:AsyncSession=Depends(get_db)):
    result= await db.execute(select(Author))
    authorlist= result.scalars().all()
    return authorlist

# get Author by Id
@author_router.get("/{id}",response_model=AuthorResponse)
async def get_author(id:int,db:AsyncSession=Depends(get_db)):
    # result = await db.execute(select(Author).where(Author.id == id))
    # author = result.scalars().first()

    author = await db.get(Author,id)
    if author is None:
        raise HTTPException(status_code=404,detail="Author not found")
    return author

# udpate author by id
@author_router.put("/{id}",response_model=AuthorResponse)
async def update_author(id:int,author_update:dict,db:AsyncSession=Depends(get_db)):
    author = await db.get(Author, id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    updateauthor=Author(**author_update)
    await db.merge(updateauthor)
    await db.commit()
    return updateauthor


#delete author by id
@author_router.delete("/{id}")
async def delete_author(id:int,db:AsyncSession=Depends(get_db)):
    author = await db.get(Author, id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    await db.delete(author)
    await db.commit()
    return {"message":"Author deleted"}





