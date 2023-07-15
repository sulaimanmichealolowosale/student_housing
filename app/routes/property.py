from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Response
from typing import Optional, List
from sqlalchemy.orm import Session
from ..schemas import *
from ..database import get_db
from ..utils import password_hash, check_not_found
from ..models import Category, Images, Property
from ..oauth2 import *
from sqlalchemy import or_, desc
import shutil


router = APIRouter(
    prefix='/property',
    tags=["Property"]
)


@router.get('/', response_model=List[GetProperty])
def manage_properies(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
    search: Optional[str] = "",
    # limit: int = 10,
    # skip: int = 0
):
    # property = db.query(Property).order_by(
    #     desc(Property.created_at)).filter(
    #     or_(Property.title.contains(search),
    #         Property.price.contains(search)
    #         )
    # ).offset(skip).limit(limit).all()

    property = db.query(Property).order_by(
        desc(Property.created_at)).filter(
        or_(Property.title.contains(search),
            Property.price.contains(search),
            Property.property_status.contains(search),
            Property.property_type.contains(search),
            Property.category_title.contains(search),
            Property.agent_nickname.contains(search)
            )
    ).all()

    check_not_found(property, id, "property")
    return property


@router.get('/get-properties/all', response_model=List[GetProperty])
def manage_users(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):

    properties = db.query(Property).all()
    return properties


@router.get('/get-properties/mine/all', response_model=List[GetProperty])
def manage_users(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):

    properties = db.query(Property).filter(
        Property.agent_id == current_user.id).all()
    return properties


@router.post('/{id}', status_code=status.HTTP_201_CREATED, response_model=GetProperty)
def manage_properies(
    id: int,
    property: AddProperty,
    current_user: str = Depends(get_current_agent),
    db: Session = Depends(get_db),
):
    category = db.query(Category).filter(Category.id == id).first()

    check_not_found(category, id, "category")

    new_property = Property(agent_id=current_user.id,
                            category_id=id,
                            agent_nickname=current_user.nick_name,
                            category_title=category.title,
                            **property.dict()
                            )
    db.add(new_property)
    db.commit()
    return new_property


@router.put('/add-primary-image/{id}', status_code=status.HTTP_201_CREATED, response_model=GetProperty)
def manage_properies(
    id: int,
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_agent),
    db: Session = Depends(get_db)
):
    property_query = db.query(Property).filter(Property.id == id)
    property_result = property_query.first()

    check_not_found(property_result, id, "post")
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"the file: {file.filename} is not an image file")

    filename_without_whitespace = file.filename.replace(" ", "_")
    with open("property_media/"+filename_without_whitespace, "wb") as image:
        shutil.copyfileobj(file.file, image)

    file_url = "property_media/"+filename_without_whitespace

    property_query.update({"primary_image_path": file_url},
                          synchronize_session=False)
    db.commit()
    return property_query.first()


@router.post('/add-images/{id}', status_code=status.HTTP_201_CREATED)
def manage_properies(
    id: int,
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_agent),
    db: Session = Depends(get_db)
):
    property = db.query(Property).filter(Property.id == id).first()

    check_not_found(property, id, "post")

    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"the file: {file.filename} is not an image file")
    filename_without_whitespace = file.filename.replace(" ", "_")
    with open("property_media/"+filename_without_whitespace, "wb") as image:
        shutil.copyfileobj(file.file, image)
    file_url = "property_media/"+filename_without_whitespace

    file_upload = Images(file_path=file_url, property_id=id)
    db.add(file_upload)
    db.commit()


@router.delete('/delete-images/all/{id}')
def manage_properies(
    id: int,
    current_user: str = Depends(get_current_agent),
    db: Session = Depends(get_db)
):

    existing_images_query = db.query(Images).filter(Images.property_id == id)
    existing_images = existing_images_query.all()

    if existing_images is not None:
        existing_images_query.delete(synchronize_session=False)
        db.commit()

    db.commit()


@router.get('/{id}', response_model=GetPropAgentImagesCat)
def manage_properies(
    id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    property = db.query(Property).filter(Property.id == id).first()
    check_not_found(property, id, "property")
    return property


@router.put('/{id}', response_model=GetProperty)
def manage_properies(
    id: int,
    category_id: int,
    property: AddProperty,
    current_user: str = Depends(get_current_agent),
    db: Session = Depends(get_db),
):
    property_query = db.query(Property).filter(Property.id == id)
    property_result = property_query.first()

    category = db.query(Category).filter(Category.id == category_id).first()

    check_not_found(category, id, "category")
    check_not_found(property_result, id, "property")

    property_dict = property.dict()

    property_dict['category_id'] = category_id
    property_dict['agent_id'] = current_user.id
    property_dict['category_title'] = category.title

    property_query.update(
        property_dict,
        synchronize_session=False
    )

    db.commit()
    return property_query.first()


@router.delete('/{id}')
def manage_properies(
        id: int,
        current_user: str = Depends(get_current_user),
        db: Session = Depends(get_db),):
    property_query = db.query(Property).filter(Property.id == id)
    property_result = property_query.first()

    check_not_found(property_result, id, "property")

    property_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete('/delete-image/{id}')
def manage_properies(
        id: int,
        current_user: str = Depends(get_current_user),
        db: Session = Depends(get_db),):
    image_query = db.query(Images).filter(Images.id == id)
    image_result = image_query.first()

    check_not_found(image_result, id, "image")

    image_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
