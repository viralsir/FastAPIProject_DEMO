from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(plain_password:str):
    return pwd_context.hash(plain_password)

def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)


# h=hash_password("Reiya@124")
# print("encrypt password base64 String :",h)
# print(verify_password("Reiya@124",h))
# print(verify_password("wrong@123",h))
