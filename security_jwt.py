from datetime import timezone, timedelta, datetime

from jose import jwt

SECRET_KEY="CHANGE-THIS-IN-PRODUCTION-AND-LOAD"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60


def create_access_token(user_id:int,role:str) ->str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub":str(user_id),"exp":expire,"role":role}
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)


def decode_access_token(token:str)->dict:
    return jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
#
# token=create_access_token(1,"customer")
# print("token:",token)
# print("decode :",decode_access_token(token))





