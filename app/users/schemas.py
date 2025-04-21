from pydantic import BaseModel, EmailStr, Field


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class SUserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=6)


class SUserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
