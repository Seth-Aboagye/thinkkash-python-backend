from pydantic import BaseModel, EmailStr

class RegisterIn(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone: str | None = None
    country: str
    role: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    verified: bool
