# from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.params import Body
# from random import randrange
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth, vote


# Using the command located below,
# whenever the app is restarted, fastapi checks for a table called 'posts'
# if it does not find it, it creates it in the DDBB, based on the predefined model.
# It only creates the table if it could not find it,
# if it's already there, it does not update it.
# You can use Alembic framework to update tables (DDBB migrations)
#
# models.Base.metadata.create_all(bind=engine)
# Since we are using alembic, this is no longer required since we are
# using alembic migrations to create or change tables

# FastAPI has built in Swagger support
# the documentation can be found at http://127.0.0.1:8000/docs
# al can be found at http://127.0.0.1:8000/redoc
app = FastAPI()

# origins = ["https://www.google.com.ar"]
# allows requests fetch('http://localhost:8000/').then(res => res.json()).then(console.log)

origins = ['*'] # allows any domain to reach our API

# Middleware is basically a function that runs for every request
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # this is the list of domains which our API is allowed to talk to
    allow_credentials=True,
    allow_methods=["*"], # not only domains, but also only some http methods could be allowed
    allow_headers=["*"],
)


# my_posts = [{"id": 1, "title": "first post title", "content": "first port content"},
#             {"id": 2, "title": "second post title", "content": "second port content"}]


# These where used to emulate a DDBB,
# and could be removed since whe are using Postgres DDBB
#
# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p
#
#
# def del_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             my_posts.remove(p)
#
#
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

# when sending HTTP requests, FA app instance returns the first path operation method it founds
# that matches the path sent in the url


# This creates a fork, including the separate files for posts and users.
# On an incoming request, it checks the request path in the added routers,
# before it continues below
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# path operation / route in other languages
@app.get("/")  # --> decorator, defines paths to go in the url
async def root():
    return {"message": "Hello World again"}


# The DB Session is sent as a parameter to the path operation function.
# This creates a session once each path method is called and closes it after the operation is completed
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    # # This is the actual SQL statement:  db.query(models.Post)
    # posts = db.query(models.Post).all()
    # return {"data": posts}
    pass




### JWT TOKENS
# For authentication, these tokens are stored in the client side


### Query parameters
# An endpoint can have query parameters
# used to filter the response
# also pagination can be done with query parameters
