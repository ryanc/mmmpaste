from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from hashlib import md5

engine = create_engine("sqlite:///db/pastebin.db")
session = scoped_session(sessionmaker(bind = engine, autoflush = False))

Base = declarative_base(bind = engine)

def init_db():
    """
    Creates the database schema. Import the models below to add them to the
    schema generation.

    Nothing happens when the database already exists.
    """
    from mmmpaste.models import Paste
    Base.metadata.create_all()


def nuke_db():
    """
    Drop the bass.
    """
    from mmmpaste.models import Paste
    Base.metadata.drop_all()


def new_paste(content, filename = None):
    from mmmpaste.models import Paste, Content
    from mmmpaste.base62 import b62_encode

    hash = md5(content).hexdigest()
    dupe = session.query(Content).filter_by(hash = hash).first()
    paste = Paste(content, filename)

    if dupe is not None:
        paste.content = dupe

    session.add(paste)
    session.commit()

    paste.id_b62 = b62_encode(paste.id)
    session.commit()

    return paste.id_b62


def get_paste(id_b62):
    from mmmpaste.models import Paste
    return session.query(Paste).filter_by(id_b62 = id_b62).first()
