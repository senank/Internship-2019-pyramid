from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Boolean,
    DateTime,
)

from PIL import Image
import os

from .meta import Base

MIMETYPE_ICONS = {
    'image/jpeg' : 'far fa-file-image',
    'image/png' : 'far fa-file-image',
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
    'text/css' : 'far fa-file-code',
    'application/json' : 'far fa-file-code',
    'application/gzip' : 'far fa-file-archive',
    'application/zip' : 'far fa-file-archive',
}

IMAGE_FORMATS = {
    'image/jpeg': '.jpg',
    'image/png': '.png'
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

    def is_image(self):
        if self.mimetype in IMAGE_FORMATS:
            return True
    

    def make_thumbnail(self, target_path, width, height):
        static_path = os.getcwd() + '/pyproj/static/uploads/'
        img = static_path + self.unique_filename
        target_path = os.path.join(static_path, target_path)
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        try:
            width = int(width)
            height = int(height)
            with Image.open(img) as f:
                w, h = f.size
                ratio = min(width/w, height/h)
                new_height = int(h*ratio)
                new_width = int(w*ratio)
                f_resized = f.resize((new_width, new_height))
                f_resized.save(target_path+self.unique_filename)
        except IOError as e:
            pass

    def generate_thumbnail(self, request, width, height):
        target_path = 'cache/{0}x{1}/'.format(width, height)
        if os.path.exists(target_path + self.unique_filename):
            return request.static_url('pyproj:static/uploads/' + target_path + self.unique_filename)
        else:
            self.make_thumbnail(target_path, width, height)
            return request.static_url('pyproj:static/uploads/' + target_path + self.unique_filename)

            


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