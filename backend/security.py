from pwdlib import PasswordHash
import jwt
from fastapi.security import OAuth2PasswordBearer
import os

password_hash=PasswordHash.recommended()
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITM="HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")