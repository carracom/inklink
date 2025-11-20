from  pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Login(BaseModel):
    email: EmailStr
    password: constr(min_length=6, max_length=255)