from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette import status

from database import get_db
from model import User
from schemas.user import UserResponse, RegisterRequest, LoginRequest
from security import hash_password, verify_password
from security_jwt import create_access_token, decode_access_token

userRouter=APIRouter()

@userRouter.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest,db:AsyncSession=Depends(get_db)):
    result =  await db.execute(select(User).where(User.email == data.email)) # asyncrhonised
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already exists")
    new_user=User(id=data.id,email=data.email,hash_password=hash_password(data.hash_password),role=data.role)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@userRouter.post("/login")
async def login(data:LoginRequest,db:AsyncSession=Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password,user.hash_password) :
        raise HTTPException(status_code=401,detail="Incorrect email or password")

    token = create_access_token(user_id=user.id,role=user.role)
    return {"access_token":token,"token_type":"bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(
        token:str = Depends(oauth2_scheme),
        db:AsyncSession = Depends(get_db)
) -> User :
    credentials_exception = HTTPException(status_code=401,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
               payload = decode_access_token(token)
               user_id = payload.get("sub")
               if user_id is None:
                   raise credentials_exception
    except JWTError:
            raise credentials_exception

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user= result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user


@userRouter.get("/profile",response_model=UserResponse)
async def profile(current_user:User = Depends(get_current_user)):
    return current_user
