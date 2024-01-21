from pydantic import BaseModel, Field, EmailStr


class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(...)
    content: str = Field(...)

    class Config:
        shema_extra = {
            "example": {
                "title": "Securing FastAPI applications with jwt.",
                "content": "With PyJWT, we'll be able to sign, encode and decode JWT tokens...",
            }
        }


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        shema_extra = {
            "example": {
                "fullname": "John Cena",
                "email": "example@email.com",
                "passowrd": "Str0ngP@55word",
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        shema_extra = {
            "example": {
                "email": "example@email.com",
                "passowrd": "Str0ngP@55word",
            }
        }