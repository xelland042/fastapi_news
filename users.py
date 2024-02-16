from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, EmailStr

from jwt_handlers import get_password_hash, signJWT, verify_password
from models import get_db, User

router = APIRouter(
)


class UserSignUpSchema(BaseModel):
    username: str
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    email: EmailStr
    password_1: str
    password_2: str


class UserLoginScheme(BaseModel):
    username: str
    password: str
    email: EmailStr


@router.post('/user/signup/', tags=['Users'])
async def user_signup(user: UserSignUpSchema, db: Session = Depends(get_db)):
    if user.password_1 != user.password_2:
        raise HTTPException(detail='Passwords should be same!', status_code=status.HTTP_400_BAD_REQUEST)
    else:
        hashed_pwd = get_password_hash(user.password_1)
        user = User(username=user.username, first_name=user.first_name, last_name=user.last_name,
                    hashed_password=hashed_pwd, email=user.email)
        db.add(user)
        db.commit()
        db.refresh(user)
        return signJWT(user.email)


@router.post('/user/login/', tags=['Users'])
async def login(user: UserLoginScheme, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user and check_user(user, db):
        return signJWT(user.email)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username, password, or email")


def check_user(data: UserLoginScheme, db: Session):
    user = db.query(User).filter(User.username == data.username).first()
    if user and verify_password(data.password, user.hashed_password) and data.email == user.email:
        return True
    return False
