import bcrypt
from uuid import uuid4
from configs.extensions import dbModel
from dependencies.security import get_hashed_password

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy import ForeignKey, Integer, Boolean, Float, String, DateTime

class Users(dbModel):
    __tablename__ = "users"

    id: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username: Mapped[str]  = mapped_column(String(128), unique=True, nullable=False)
    email: Mapped[str]  = mapped_column(String(128), unique=True, nullable=True)
    phone_number: Mapped[str]  = mapped_column(String(12), unique=True, nullable=True)
    password: Mapped[str]  = mapped_column(String(256), nullable=False)
    full_name: Mapped[str]  = mapped_column(String(256), nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, unique=False, nullable=False, default=False)
    number_verified: Mapped[bool] = mapped_column(Boolean, unique=False, nullable=False, default=False)
    active: Mapped[bool]  = mapped_column(Boolean, unique=False, nullable=False, default=False)

    def __init__(self, username, email, phone_number, password, full_name):
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.password = get_hashed_password(password)
        self.full_name = full_name
        self.email_verified = False
        self.number_verified = False
        self.active = False

    
    def __repr__(self):
        return f'<Users {self.username}>'
    
