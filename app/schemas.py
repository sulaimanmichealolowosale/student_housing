from pydantic import BaseModel, EmailStr, constr, conint, Field
from typing import Optional, List
from datetime import datetime

###################################### AUTH SCHEMAS ########################################


class TokenData(BaseModel):
    id: str


class Auth(BaseModel):
    username: str
    password: str


class GetAuthDetails(BaseModel):
    id: int
    first_name: str
    last_name: str
    nick_name: str
    email: EmailStr
    phone:str
    role: str
    image_url: str
    access_token: str

    class Config:
        orm_mode = True


###################################### USER SCHEMAS ########################################

class CreateUser(BaseModel):
    first_name: constr(strict=True, strip_whitespace=True)
    last_name: constr(strict=True, strip_whitespace=True)
    nick_name: str
    email: EmailStr
    phone: constr(strict=True, strip_whitespace=True, max_length=11)
    role: str = "student"
    password: constr(strip_whitespace=True,
                     min_length=8, max_length=20)


class GetUsers(BaseModel):
    id: int
    first_name: str
    last_name: str
    nick_name: str
    email: EmailStr
    phone: str
    role: str
    rating: int
    image_url: str
    created_at: datetime

    class Config:
        orm_mode = True

###################################### CATEGORY SCHEMAS ########################################


class AddCategory(BaseModel):
    title: str = Field(description="category name gangan")
    description: str


class GetCategory(BaseModel):
    id: int
    title: str
    agent_id: int
    agent_nickname:str
    description: Optional[str] = ""
    created_at: datetime

    class Config:
        orm_mode = True

###################################### PROPERTY SCHEMAS ########################################


class AddProperty(BaseModel):
    title: str = Field(default="A room self-contained",
                       description="eg: single single room, room self-contained")
    description: str = Field(default="The room is a 10X10 room with a 24 inches plasma tv and a standing fan",
                             description="this includes the property details(size, and other features it offers),and distance from school")
    address: str = Field(default="school two",
                         description="eg: school two, deuteronomy etc.")
    security_type: str = Field(
        default="Fenced with security personnel", description="eg: front and back metal door")
    water_system: str = Field(
        default="Tap water", description="eg: tap water, well water")
    toilet_bathroom_desc: str = Field(
        default="One bathroom and one toilet", description="eg: One bathroom and one toilet")
    kitchen_desc: str = Field(default="One kitchen for one appartment",
                              description="eg: One kitchen for one appartment")
    property_status: str = Field(
        default="available", description="eg: available, unavailable")
    property_type: str = Field(
        default="rent", description="eg: rent, sale, lease")
    price: str = Field(default="90,000", description="eg: 90,000")
    payment_duration: str = Field(
        default="per session", description="eg: per month")
    additional_fee: str = Field(
        default="1,000", description="enter fee withouth including the currency")
    reason_for_fee: str = Field(
        default="for form", description="A breakdown of the additional fee")
    agent_phone: str = Field(default="09067534592",
                             description="Phone number", max_length=11)


class GetImages(BaseModel):
    id: int
    file_path: str
    property_id: int

    class Config:
        orm_mode = True


class GetProperty(BaseModel):
    id: int
    title: str
    description: str
    address: str
    security_type: str
    water_system: str
    toilet_bathroom_desc: str
    kitchen_desc: str
    property_status: str
    property_type: str
    price: str
    payment_duration: str
    additional_fee: str
    reason_for_fee: Optional[str] = ""
    primary_image_path: Optional[str] = ""
    agent_id: int
    agent_phone: str
    agent_nickname: str
    category_id: int
    category_title:Optional[str]=""
    created_at: datetime

    class Config:
        orm_mode = True


###################################### RELATIONSHIP SCHEMAS ########################################

class GetPropAgentImagesCat(GetProperty):
    agent: GetUsers
    category: GetCategory
    images: List[GetImages]


class GetCatWithAgentAndProps(GetCategory):
    agent: GetUsers
    properties: List[GetProperty]


class GetUserWithCatAndProp(GetUsers):
    categories: List[GetCategory]
    properties: List[GetProperty]
