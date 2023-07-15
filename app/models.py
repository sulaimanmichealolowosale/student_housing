from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    nick_name = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default="student")
    email = Column(String, nullable=False)
    rating = Column(Integer, nullable=True, server_default=text("0"))
    phone = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text('CURRENT_TIMESTAMP'))
    properties = relationship("Property")
    categories = relationship("Category")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    agent_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    agent_nickname = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text('CURRENT_TIMESTAMP'))

    agent = relationship("User", foreign_keys=agent_id,
                         back_populates="categories")
    properties = relationship("Property")


class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    address = Column(String, nullable=False)
    security_type = Column(String, nullable=False)
    water_system = Column(String, nullable=False)
    toilet_bathroom_desc = Column(String, nullable=False)
    kitchen_desc = Column(String, nullable=False)
    property_status = Column(String, nullable=False)
    property_type = Column(String, nullable=False)
    price = Column(String, nullable=False)
    payment_duration = Column(String, nullable=False)
    additional_fee = Column(String, nullable=True)
    reason_for_fee = Column(String, nullable=True)
    primary_image_path = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey(
        "categories.id", ondelete="CASCADE"), nullable=False)
    category_title = Column(String, nullable=True)
    agent_phone = Column(String, nullable=True)
    agent_nickname = Column(String, nullable=True)
    agent_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text('CURRENT_TIMESTAMP'))

    agent = relationship("User", foreign_keys=agent_id,
                         back_populates="properties")
    category = relationship(
        "Category", foreign_keys=category_id, back_populates="properties")
    images = relationship("Images")


class Images(Base):
    __tablename__ = "property_images"
    id = Column(Integer, primary_key=True, nullable=False)
    file_path = Column(String, nullable=False)
    property_id = Column(Integer, ForeignKey(
        "properties.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text('CURRENT_TIMESTAMP'))
