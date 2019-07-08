from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Boolean,
    DateTime,
)

from .meta import Base


class TodoItem(Base):
    __tablename__ = 'todo_item'
    id = Column(Integer, primary_key=True)
    #user_id = Column(Integer)
    description = Column(Text)
    completed = Column(Boolean, nullable=False, default=False, server_default=u'false', index=True)
    position = Column(Integer, nullable=False, default=0, server_default=u'0', index=True)
    completed_date = Column(DateTime)
    created_date = Column(DateTime, nullable=False)


Index('todo_item_idx', TodoItem.completed.asc(), TodoItem.position.desc(), unique=False)


#select * from todo_item as t 
#where user_id = 10
#order by t.completed asc, t.position desc
#
#[ ] task 1
#[ ] task 2
#[ ] task 3
#[x] task 10
#[x] task 11
#[x] task 20
