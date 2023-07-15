from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Response
from typing import Optional, List
from sqlalchemy.orm import Session
from ..schemas import *
from ..database import get_db
from ..utils import password_hash, check_not_found
from ..models import User
from ..oauth2 import get_current_user, get_current_admin
from sqlalchemy import or_
import shutil


router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@router.post("/", response_model=GetUsers, status_code=status.HTTP_201_CREATED)
def manage_users(user: CreateUser, db: Session = Depends(get_db)):
    hashed_password = password_hash(user.password)
    user.password = hashed_password

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"The user with email {user.email} already exist")

    new_user = User(image_url="user_media/defaultuser.png", **user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/', response_model=List[GetUsers])
def manage_users(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
    search: Optional[str] = "",
    # limit: int = 10,
    # skip: int = 0
):
    users = ""
    if current_user.role == "student" or current_user.role == "agent":
        users = db.query(User).filter(
            User.role != "admin",
            User.role != "student",
            User.nick_name.contains(search)
        ).all()

    elif current_user.role == "admin" or current_user.role == "superuser":
        users = db.query(User).filter(
            or_(
                User.nick_name.contains(search),
                User.role.contains(search)
            )
        ).all()

    return users


@router.get('/get-users/all', response_model=List[GetUsers])
def manage_users(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):

    users = db.query(User).all()
    return users


@router.get('/agents', response_model=List[GetUsers])
def manage_users(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
    search: Optional[str] = "",

):

    users = db.query(User).filter(
        or_(
            User.role == "agent",
            User.role == "superuser"
        ),
        User.nick_name.contains(search)
    ).all()
    return users


@router.get('/{id}', response_model=GetUserWithCatAndProp)
def manage_user(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id).first()
    check_not_found(user, id, "user")
    return user


@router.put('/{id}', response_model=GetUsers)
def manege_users(id: int, user: CreateUser, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user_query = db.query(User).filter(User.id == id)
    user_result = user_query.first()

    existing_email = db.query(User).filter(User.email == user.email).first()

    check_not_found(user_result, id, "user")

    if existing_email and id != existing_email.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already taken")

    hashed_password = password_hash(user.password)
    user.password = hashed_password

    user_query.update(user.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()


@router.put('/update-profile-picture/{id}')
def manage_user(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user),
                file: UploadFile = File(...)):
    user_query = db.query(User).filter(User.id == id)
    user_result = user_query.first()

    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"the file: {file.filename} is not an image file")

    filename_without_whitespace = file.filename.replace(" ", "_")
    with open("user_media/"+filename_without_whitespace, "wb") as image:
        shutil.copyfileobj(file.file, image)
    image_url = "user_media/"+filename_without_whitespace

    user_query.update({"image_url": image_url}, synchronize_session=False)
    db.commit()
    return user_query.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def manage_users(id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_admin)):

    user_query = db.query(User).filter(User.id == id)
    user_result = user_query.first()

    check_not_found(user_result, id, "user")
    user_query.delete(synchronize_session=False)

    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
