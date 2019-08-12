from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Boolean,
    DateTime,
)

from .meta import Base

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(Text, nullable = False)
    password = Column(Text, nullable = False)
    permissions = Column(Text, nullable = True)