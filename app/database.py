# SQLAlchemy is used as ORM (object relational model).
# Using ORMS, tables are defined as python classes,
# and all the sql statements are sent by writing python code the ORM layer,
# and finally sent to the DDBB as sql sentences.
# https://www.sqlalchemy.org/
# https://fastapi.tiangolo.com/tutorial/sql-databases/

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# libraries for Postgres DDBB connection without sqlAlchemy
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# CONN STRING
# format: 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
# SQL_ALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/fastapi'

# Using env variables
SQL_ALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}' \
                           f'@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# SQL ALCHEMY ENGINE
# Responsible for establishing a connection to the postgresql database
engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

# SESSION
# talk to sql database through a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# BASE CLASS
# all the models created to define tables, are going to extend this base class
Base = declarative_base()


# Dependency
# This gets a session to the DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# This piece of code is the implementation of the DDBB connection to Postgres directly,
# without SQL alchemy
# we keep it in our database module, but just for documentation.
# It can be removed since SQL alchemy is handling the connection anyway.

# DB CONNECTION
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',
#                                 database='fastapi',
#                                 user='postgres',
#                                 password='admin',
#                                 cursor_factory=RealDictCursor)
#                                 ## with this the cursor includes the column name, creating a dict
#         cursor = conn.cursor()
#         print("Database connection successfull")
#         break
#     except Exception as error:
#         print('Connection to the Database failed')
#         print("Error: ", error)
#         time.sleep(2)
