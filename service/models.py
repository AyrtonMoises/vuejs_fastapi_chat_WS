from sqlalchemy import Column, Integer, String, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base, engine


metadata = Base.metadata

room_users_table = Table(
    "room_users",
    Base.metadata,
    Column("room_id", ForeignKey("room.id", ondelete="CASCADE")),
    Column("user_id", ForeignKey("user.id")),
    UniqueConstraint('room_id', 'user_id', name='room_user_unique'),

)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    rooms = relationship('Room',
        secondary=room_users_table,
        backref='room_users', viewonly=True
    )  

class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    users = relationship(
        "User", secondary=room_users_table, backref='room_users', cascade="all, delete", single_parent=True
    )

Base.metadata.create_all(bind=engine)