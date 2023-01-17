from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Room, User
from schemas import RoomInSchema, UserSchema


class RoomCRUD():

    def __init__(self, db: Session):
        self.db = db

    def create(self, room: RoomInSchema):
        db_room = Room(
            title=room.title
        )
        self.db.add(db_room)
        self.db.commit()
        self.db.refresh(db_room)

        return db_room

    def get_all(self):
        rooms = self.db.query(Room).all()
        return rooms

    def get(self, room_id: int):
        room = self.db.query(Room).filter(Room.id==room_id).one_or_none()

        if room is None:
            raise HTTPException(status_code=404, detail="room not found")

        return room



class UserCRUD():

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: UserSchema):
        db_user = User(
            username=user.username,
            password=user.password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def get_all(self):
        users = self.db.query(User).all()
        return users

    def get(self, user_id: int):
        user = self.db.query(User).filter(User.id==user_id).one_or_none()

        if user is None:
            raise HTTPException(status_code=404, detail="user not found")

        return user

    def update(self, user_id: int):
        stmt = select(User).filter_by(id=user_id)
        user = self.db.execute(stmt).one()

        return user

    def delete(self, username: str):
        user = self.db.query(User).filter(User.username==username)

        if user.one_or_none() is None:
            raise HTTPException(status_code=404, detail="user not found")

        user.delete()
        self.db.commit()

    def update(self, user_id: int, user_data: User):
        user = self.db.query(User).filter(User.id==user_id).one_or_none()

        if user is None:
            raise HTTPException(status_code=404, detail="user not found")

        user.username = user_data.username
        user.password = user_data.password

        self.db.commit()
        self.db.refresh(user)
        return user

    def validate_user(self, user_data: User):
        user = self.db.query(User).filter(User.username==user_data.username,User.password==user_data.password).one_or_none()

        if user is None:
            raise HTTPException(status_code=404, detail="user not found")

        return user