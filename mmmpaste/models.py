import datetime
import re

from hashlib import md5

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import DateTime, Integer, String, Text, CHAR, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy import event

from mmmpaste.db import Base

class Paste(Base):
    __tablename__ = "pastes"

    id = Column(Integer, primary_key = True, nullable = False)
    id_b62 = Column(String(20), unique = True)
    filename = Column(String(50))
    content_id = Column(Integer, ForeignKey('paste_content.id'))
    created_at = Column(DateTime, nullable = False, default = datetime.datetime.now)
    modified_at = Column(DateTime, onupdate = datetime.datetime.now)
    highlight = Column(Boolean, nullable = False, default = True)
    content = relationship("Content")

    def __init__(self, filename = None, highlight = True):
        self.filename = filename
        self.highlight = highlight

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

    convert_tabs = True

    def __init__(self, content, convert_tabs = True):
        self.convert_tabs = convert_tabs
        self.content = content
        self.hash = md5(content).hexdigest()

    def __repr__(self):
        truncated = (self.content[:25] + "...") if len(self.content) > 25 \
                                                else self.content
        return "<Content %r %r %r>" % (self.id, self.hash, truncated)

    def __str__(self):
        return self.content


def tabs_to_spaces(target, value, oldvalue, initiator):
    if target.convert_tabs:
        return re.sub(r"\t", " " * 4, value)

    return value


event.listen(Content.content, "set", tabs_to_spaces, retval = True)
