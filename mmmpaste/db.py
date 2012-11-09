import contextlib

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
    from mmmpaste.models import Paste, Content
    Base.metadata.create_all()


def nuke_db():
    """
    Drop the bass.
    """
    from mmmpaste.models import Paste, Content
    Base.metadata.drop_all()


def empty_db():
    """
    Clear the tables, but do not drop the schema.
    """
    from mmmpaste.models import Paste, Content
    with contextlib.closing(engine.connect()) as conn:
        transaction = conn.begin()
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
        transaction.commit()


def new_paste(content, ip_addr, filename = None, highlight = True, convert_tabs = True):
    from mmmpaste.models import Paste, Content
    from mmmpaste.base62 import b62_encode

    paste = Paste(ip_addr, filename, highlight)
    paste.content = Content(content, convert_tabs)

    hash = paste.content.hash
    dupe = session.query(Content).filter_by(hash = hash).first()

    if dupe is not None:
        paste.content = dupe

    session.add(paste)
    session.flush()

    paste.id_b62 = b62_encode(paste.id)
    session.commit()

    return paste.id_b62


def get_paste(id_b62 = None):
    """
    Get the paste for the given base 62 id.
    """
    from mmmpaste.models import Paste
    if id_b62 is None:
        return session.query(Paste).order_by(Paste.id.desc()).first()

    return session.query(Paste).filter_by(id_b62 = id_b62).first()
