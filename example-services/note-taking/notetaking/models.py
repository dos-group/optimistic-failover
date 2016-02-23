from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    msgid = Column(Text)
    content = Column(Text)
    timestamp = Column(Text)

class DelMessage(Base):
    __tablename__ = 'del_messages'
    id = Column(Integer, primary_key=True)
    msgid = Column(Text)
    timestamp = Column(Text)

Index('my_index', MyModel.name, unique=True, mysql_length=255)

Index('msg_index', Message.msgid, unique=True, mysql_length=255)
Index('del_msg_index', DelMessage.msgid, unique=True, mysql_length=255)


