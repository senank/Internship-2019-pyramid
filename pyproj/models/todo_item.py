from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Boolean,
    DateTime,
)

from .meta import Base

MIMETYPE_ICONS = {
    'image/jpeg' : 'far fa-file-image',
    'audio' : 'far fa-file-audio',
    'video' : 'far fa-file-video',
    'application/pdf' : 'far fa-file-pdf',
    'application/msword' : 'far fa-file-word',
    'application/vnd.ms-word' : 'far fa-file-word',
    'application/vnd.oasis.opendocument.text' : 'far fa-file-word',
    'application/vnd.openxmlformats-officedocument.wordprocessingml' : 'far fa-file-word',
    'application/vnd.ms-excel' : 'far fa-file-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml' : 'far fa-file-excel',
    'application/vnd.oasis.opendocument.spreadsheet' : 'far fa-file-excel',
    'application/vnd.ms-powerpoint' : 'far fa-file-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml' : 'far fa-file-powerpoint',
    'application/vnd.oasis.opendocument.presentation' : 'far fa-file-powerpoint',
    'text/plain' : 'far fa-file-alt',
    'text/html' : 'far fa-file-code',
    'application/json' : 'far fa-file-code',
    'application/gzip' : 'far fa-file-archive',
    'application/zip' : 'far fa-file-archive',
}


class TodoItem(Base):
    __tablename__ = 'todo_item'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    completed = Column(Boolean, nullable=False, default=False, server_default=u'false', index=True)
    position = Column(Integer, nullable=False, index=True)
    created_date = Column(DateTime, nullable=False)
    completed_date = Column(DateTime)
    filename = Column(Text)
    unique_filename = Column(Text)
    mimetype = Column(Text)
    

    def get_icon(self):
        icon = MIMETYPE_ICONS.get(self.mimetype, 'far fa-file')
        return icon


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