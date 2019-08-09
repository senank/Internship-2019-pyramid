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
    # __table_args_ = {extend_existing : True}
    user_id = Column(Integer, primary_key=True)
    first_name = Column(Text)
    last_name = Column(Text)
    permissions = Column(Text)