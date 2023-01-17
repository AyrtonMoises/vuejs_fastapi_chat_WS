from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas import UserSchema, RoomInSchema, RoomOutSchema
from database import get_db
from crud import UserCRUD, RoomCRUD



router = APIRouter()

# User
@router.post('/users', response_model=UserSchema, status_code=status.HTTP_201_CREATED, tags=["user"])
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    user = UserCRUD(db).create(user)
    return user

@router.get('/users', response_model=List[UserSchema], tags=["user"])
def get_all_users(db: Session = Depends(get_db)):
    return UserCRUD(db).get_all()

@router.get('/users/{user_id}', response_model=UserSchema, tags=["user"])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UserCRUD(db).get(user_id)
    return user

@router.put("/users/{user_id}", response_model=UserSchema, tags=["user"])
def update_user(user_id: int, user: UserSchema, db: Session = Depends(get_db)):
    return UserCRUD(db).update(user_id, user)

@router.delete('/users/{username}', tags=["user"])
def delete_user(username: str, db: UserSchema = Depends(get_db)):
    UserCRUD(db).delete(username)
    return {"msg": "Success"}

# Auth
@router.post('/login', response_model=UserSchema, status_code=status.HTTP_201_CREATED, tags=["auth"])
def login_user(user: UserSchema, db: Session = Depends(get_db)):
    user = UserCRUD(db).validate_user(user)
    return user

# Rooms
@router.post('/rooms', response_model=RoomOutSchema, status_code=status.HTTP_201_CREATED, tags=["room"])
def create_room(room: RoomInSchema, db: Session = Depends(get_db)):
    room = RoomCRUD(db).create(room)
    return room

@router.get('/rooms', response_model=List[RoomOutSchema], tags=["room"])
def get_all_rooms(db: Session = Depends(get_db)):
    return RoomCRUD(db).get_all()

@router.get('/rooms/{room_id}', response_model=RoomOutSchema, tags=["room"])
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = RoomCRUD(db).get(room_id)
    return room