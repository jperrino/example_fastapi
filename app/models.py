# Every model represents a table in Python
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


# The SQLAlchemy model
# Defines tables structure (field, values)
# Is different from the Pydantic models
class Post(Base):
    # specify table name in the DDBB
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # sqlAlchemy limitations!!!!
    # If we change the table model, but the table already exists with a different model,
    # sqlAlchemy does not change de table in the DDBB, it does nothing
    # The table can be dropped to pickup the change
    # Basically, sqlAlchemy does not update the tables based on the model,
    # It just creates the table based on the model if it does found a table with
    # the given name when the application starts
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # We can set up relationships between the models, these do not affect our schema,
    # and it's only used in sqlAlchemy to modify the schemas returned in each request
    owner = relationship('User')

    # In order to bypass the sqlAlchemy limitation about not updating tables,
    # a new tool is required: Alembic (database migration tool)
    # url: https://alembic.sqlalchemy.org/en/latest/


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete='CASCADE'), primary_key=True)
