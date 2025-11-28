from sqlalchemy import Column, Integer, String, ForeignKey
from upscales.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

