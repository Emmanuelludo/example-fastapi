from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Integer
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Post(Base):
    __tablename__ = 'PostsOrm'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        'Users.id', ondelete='CASCADE',), nullable=False)
    owner = relationship('User')


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Votes(Base):
    __tablename__ = 'Votes'
    user_id = Column(Integer, ForeignKey(
        'Users.id', ondelete='CASCADE',), primary_key=True,)
    post_id = Column(Integer, ForeignKey(
        'PostsOrm.id', ondelete='CASCADE',), primary_key=True,)
