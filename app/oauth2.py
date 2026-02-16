import fastapi.security.oauth2
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.routers.auth import login
from sqlalchemy.orm import Session
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer



#This takes the information coming from the user when he logs in
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "8f754629a528da61e70d69ed096df5420f293e2d7918465d5bbfc288369dcb7f"
ALGORITHM =  "HS256"
ACCESS_TOKEN_EXPIRATION_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if not id:
            raise credentials_exception
        #Token data is just the ID for now, but we can add other fields to this if we want
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user