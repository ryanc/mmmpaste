import datetime

from hashlib import md5

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import DateTime, Integer, String, Text, CHAR
from sqlalchemy.orm import relationship, backref

from mmmpaste.db import Base

class Paste(Base):
    __tablename__ = "pastes"

    id = Column(Integer, primary_key = True, nullable = False)
    id_b62 = Column(String(20), unique = True)
    filename = Column(String(50))
    content_id = Column(Integer, ForeignKey('paste_content.id'))
    created_at = Column(DateTime, nullable = False, default = datetime.datetime.now)
    modified_at = Column(DateTime, onupdate = datetime.datetime.now)
    content = relationship("Content")

    def __init__(self, content, filename = None):
        self.content = content
        self.filename = filename

    def __repr__(self):
        return "<Paste %r, %r, %r>" % (self.id, self.id_b62, self.filename)

    def __str__(self):
        return str(self.content)

class Content(Base):
    __tablename__ = "paste_content"

    id = Column(Integer, primary_key = True, nullable = False)
    hash = Column(CHAR(32), unique = True, nullable = False)
    created_at = Column(DateTime, nullable = False, default = datetime.datetime.now)
    modified_at = Column(DateTime, onupdate = datetime.datetime.now)
    content = Column(Text, unique = True, nullable = False)

    def __init__(self, content):
        self.content = content
        self.hash = md5(content).hexdigest()

    def __repr__(self):
        truncated = (self.content[:25] + "...") if len(self.content) > 25 \
                                                else self.content
        return "<Content %r %r %r>" % (self.id, self.hash, truncated)
    def __str__(self):
        return self.content
