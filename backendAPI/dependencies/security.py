import base64
from jose import jwt, jws
from fastapi import HTTPException, Depends, Request
import os
from jose import jwt
from typing import Union, Any
from configs.config import Config
from datetime import datetime, timedelta
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)

