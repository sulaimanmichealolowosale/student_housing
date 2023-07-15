from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas import GetAuthDetails
from ..database import get_db
from ..models import User
from ..utils import verify_password
from ..oauth2 import create_access_token
from ..oauth2 import get_current_user
from datetime import timedelta

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post('/', response_model=GetAuthDetails)
def auth(login_details: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_query = db.query(User).filter(User.email == login_details.username)
    user_result = user_query.first()

    if user_result is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not verify_password(login_details.password, user_result.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = create_access_token(
        data={"nick_name": user_result.nick_name, "role": user_result.role})

    return {
        "id": user_result.id,
        "first_name": user_result.first_name,
        "last_name": user_result.last_name,
        "email": user_result.email,
        "phone": user_result.phone,
        "nick_name": user_result.nick_name,
        "image_url": user_result.image_url,
        "role": user_result.role,
        "access_token": access_token
    }

# @router.get('/logout')
# def logout(response: Response, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
#     response.delete_cookie("access_token")
#     response.delete_cookie("refresh_token")

#     user_query = db.query(User).filter(User.staff_id == current_user.staff_id)
#     user_result = user_query.first()

#     user_query.update({"active": 0}, synchronize_session=False)
#     db.commit()
#     return {"message": "Loggged out"}
