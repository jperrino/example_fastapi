from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

"""
    START POST ROUTES/PATH OPERATIONS
"""

# limit is used as a parameter to define how many posts will be retieved
# skip is used as pagination to remove the initial results from the query
# the search tries to find keywords in the Post text


# @router.get("/", response_model=List[schemas.PostResponse])  # --> decorator, defines paths to go in the url
# Added new Response model 'PostWithVotesResponse' used to validate the Post response with the votes field
@router.get("/", response_model=List[schemas.PostWithVotesResponse])
async def get_posts(db: Session = Depends(get_db),
                    current_user = Depends(oauth2.get_current_user),
                    limit: int = 3,
                    skip: int = 0,
                    search: Optional[str] = ""):
    # cursor.execute("""
    #                 SELECT * FROM posts
    #                 """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # print(limit)
    # We can also filter the posts retrieved to only show the posts
    # created by that specific user, instead of retrieving all
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    # return {"data": posts}  # --> serialization is done automatically

    # SQLAlchemy uses by default INNER JOINS
    results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote,
                                         models.Vote.post_id == models.Post.id,
                                         isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)
    return results


# In order not to interfere with other routes with similar paths,
# the controllers have to be placed from top to down to prevent errors.
# FastAPI always picks the first controller that matches the path
@router.get("/latest")  # --> the {id} of the post to retrieve is embedded in the url, {id} is a path parameter
async def get_latest_post():
    # post = my_posts[len(my_posts)-1]
    # return {"message": f"Here's the post: {post}"}  # --> serialization is done automatically
    pass


# @router.get("/{id}", response_model=schemas.PostResponse)  # --> the {id} of the post to retrieve is embedded in the url, {id} is a path parameter
# Added new Response model 'PostWithVotesResponse' used to validate the Post response with the votes field
@router.get("/{id}", response_model=schemas.PostWithVotesResponse)
async def get_post(id: int, db: Session = Depends(get_db),
                   current_user = Depends(oauth2.get_current_user)):  # --> response: Response is not needed atm
    # cursor.execute("""
    #             SELECT * from posts WHERE id = %s
    #             """, (str(id)))
    # post = cursor.fetchone()

    # Old query to retrieve post without JOIN
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # New query to retrieve post with JOIN
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote,
                                                                                         models.Vote.post_id == models.Post.id,
                                                                                         isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # print(id)
    # post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} was not found"}
    # return {"message": f"Here's the post: {post}"}  # --> serialization is done automatically
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)  # when sending a 204, no content should be sent back
async def delete_post(id: int, db: Session = Depends(get_db),
                      current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""
    #             DELETE * from posts WHERE id = %s RETURNING *
    #             """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # deleting post
    # del_post(id)
    # index = find_index_post(id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exists")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not Authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    # my_posts.pop(index)
    # return {'message': f"Post with id: {id} successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)  # --> the {id} of the post to retrieve is embedded in the url, {id} is a path parameter
async def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db),
                      current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""
    #             UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *
    #             """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # index = find_index_post(id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exists")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not Authorized to perform requested action")

    # to update, we convert the post to a dictionary and send it as a parameter
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    # # convert received post into a dictionary
    # post_dict = post.dict()
    # post_dict['id'] = id
    # # Post object does not have an id in its properties, the id added upon creation
    # # when updating the post we are actually creating a new one and replacing the existing post
    # # so the id of the previous post needs to be added as well, if not, the new post would
    # # not have an id to be identified
    # my_posts[index] = post_dict
    # return {'data': updated_post}
    return post_query.first()


# async def create_post(payload: dict = Body(...)):
# --> takes the request Body and saves it to payload variable (type dict)
# print(payload)
# return {"message": "Successfully created a post",
#         "title": f"{new_post['title']}",
#         "content": f"{new_post['content']}"}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)  # --> decorator, defines paths to go in the url
async def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db),
                      current_user = Depends(oauth2.get_current_user)):  # new_post holds an instance of Post, and the payload schema is validated
    # print(new_post)
    # print(new_post.published)
    # print(new_post.dict())  # built in dict() method transform the instance into a python dictionary
    #
    # # This method prevents from SQL injection
    # cursor.execute("""
    # INSERT INTO posts (title, content,published) VALUES (%s,%s,%s) RETURNING *
    # """, (new_post.title, new_post.content, new_post.published))
    # # Returns the last inserted row, returned to the cursor
    # post_returned_from_cursor = cursor.fetchone()
    # # Commit changes to DB
    # conn.commit()
    #
    # Create new post using ORM
    #
    # In this way, all the post fields need to be mapped manually
    # new_post_to_db = models.Post(title=new_post.title, content=new_post.content, published=new_post.published)
    # This method, unpacks the dictionary and returns the post object in the same format as above (pydantic model)
    print(current_user.email)
    # Adding the id retrieved from the token, to fill the owned_ir field
    new_post_to_db = models.Post(owner_id=current_user.id, **new_post.dict())
    db.add(new_post_to_db)
    db.commit()
    db.refresh(new_post_to_db)  # retrieve recently created post and store it in new_post variable
    # post_dict = new_post.dict()
    # post_dict['id'] = randrange(0, 10000)
    # my_posts.append(post_dict)
    # return {"message": "Successfully created a post",
    #         "title": f"{new_post.title}",
    #         "content": f"{new_post.content}"}
    # return {"data": post_returned_from_cursor}
    return new_post_to_db


# In order to get not to get into problems with what the client sends to the API,
# it is required to define a 'schema' and validate that the body of the request
# follows that schema, else returning an error.
# Define schema --> pydantic

"""
    END POST ROUTES/PATH OPERATIONS
"""