from uuid import UUID
from typing import Optional
from pydantic import BaseModel, validator, root_validator, ValidationError

class UserInfo(BaseModel):
    id: UUID
    username : str
    full_name: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    email_verified: bool
    number_verified: bool
    active: bool
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "abcd123",
                "username": "johndoe",
                "full_name": "John Doe",
                "email": "johndoe@gmail.com",
                "phone_number": "987654321",
                "email_verified": True,
                "number_verified": True,
                "active": True,
            }
        }

class UserSingup(BaseModel):
    email: str | None = None
    phone_number: str | None = None
    username : str
    full_name: str
    password: str
    
    @root_validator(pre=True)
    def check_email_or_phone(cls, values):
        email = values.get('email')
        phone_number = values.get('phone_number')
        if not email and not phone_number:
            raise ValueError('Either email or phone number must be provided.')
        return values

    class Config:
        json_schema_extra = {
            "example": {
                "email": "dummy@mail.com",
                "phone_number": "987654321",
                "username": "demo_user",
                "full_name": "John Doe",
                "password": "password",
            }
        }

class UserLogin(BaseModel):
    email: Optional[str] | None = None
    phone_number: Optional[str] | None = None
    username : Optional[str] | None = None
    password: str
    
    @root_validator(pre=True)
    def check_email_or_phone_or_username(cls, values):
        email = values.get('email')
        phone_number = values.get('phone_number')
        username = values.get('username')
        if not email and not phone_number and not username:
            raise ValueError('Either email/username or phone number must be provided.')
        return values

    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "987654321",
                "password": "password",
            }
        }

class ResendOTP(BaseModel):
    email: Optional[str] | None = None
    phone_number: Optional[str] | None = None
    
    @root_validator(pre=True)
    def check_email_or_phone(cls, values):
        email = values.get('email')
        phone_number = values.get('phone_number')
        if not email and not phone_number:
            raise ValueError('Only one of  +email or phone number must be provided.')
        if email and phone_number:
            raise ValueError('Only one of email or phone number must be provided.')
        return values
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "987654321"
            }
        }

class VerifySingup(BaseModel):
    email: Optional[str] | None = None
    phone_number: Optional[str] | None = None
    otp: str
    
    @root_validator(pre=True)
    def check_email_or_phone(cls, values):
        email = values.get('email')
        phone_number = values.get('phone_number')
        if not email and not phone_number:
            raise ValueError('Only one of  +email or phone number must be provided.')
        if email and phone_number:
            raise ValueError('Only one of email or phone number must be provided.')
        return values
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "987654321",
                "otp": "123456"
            }
        }