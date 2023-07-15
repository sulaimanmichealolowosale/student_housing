from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Response
from typing import Optional, List
from sqlalchemy.orm import Session
from ..schemas import *
from ..database import get_db
from ..utils import password_hash, check_not_found
from ..models import Category
from ..oauth2 import get_current_user, get_current_admin, get_current_agent
from sqlalchemy import or_, desc
import shutil


router = APIRouter(
    prefix='/category',
    tags=["Category"]
)


@router.post('/', response_model=GetCategory, status_code=status.HTTP_201_CREATED)
def manage_properies(category: AddCategory, db: Session = Depends(get_db), current_user: str = Depends(get_current_agent)):
    existing_category = db.query(Category).filter(
        Category.title == category.title).first()

    if existing_category is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"The category with title {category.title} already exist")

    new_category = Category(agent_id=current_user.id,
                            agent_nickname=current_user.nick_name, **category.dict())
    db.add(new_category)
    db.commit()
    return new_category


@router.get('/', response_model=List[GetCategory])
def manage_categories(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
    search: Optional[str] = "",
):
    categories = db.query(Category).order_by(
        desc(Category.created_at)).filter(
        or_(
            Category.title.contains(search),
            Category.agent_nickname.contains(search)
        )).all()
    return categories


@router.get('/get-categories/all', response_model=List[GetCategory])
def manage_users(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):

    categories = db.query(Category).all()
    return categories


@router.get('/get-categories/mine/all', response_model=List[GetProperty])
def manage_users(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):

    properties = db.query(Category).filter(
        Category.agent_id == current_user.id).all()
    return properties


@router.get('/{id}', response_model=GetCatWithAgentAndProps)
def manage_category(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user),):
    category = db.query(Category).filter(Category.id == id).first()
    check_not_found(category, id, "category")
    return category


@router.put('/{id}', response_model=GetCategory)
def manage_category(category: AddCategory, id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_agent),):
    category_query = db.query(Category).filter(Category.id == id)
    category_result = category_query.first()
    check_not_found(category_result, id, "category")

    existing_category = db.query(Category).filter(
        Category.title == category.title).first()
    if existing_category and id != existing_category.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Category already exists")

    category_query.update(category.dict(), synchronize_session=False)
    db.commit()
    return category_query.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def manage_category(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_admin)):
    category_query = db.query(Category).filter(Category.id == id)
    category_result = category_query.first()
    check_not_found(category_result, id, "category")

    category_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
