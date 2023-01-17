from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class RoomInSchema(BaseModel):
    title: str

    class Config:
        orm_mode = True

class RoomOutSchema(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True