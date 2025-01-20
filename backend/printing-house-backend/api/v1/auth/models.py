from pydantic import BaseModel, EmailStr, constr


class RegisterUser(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    first_name: str
    last_name: str
    phone_number: str


class LoginUser(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class LoginResponse(BaseModel):
    email: EmailStr
    access_token: str
