from app import models, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app.oauth2 import get_current_user
from .. import oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     #print(posts)
#     return {"data" : posts}



@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              limit: int =10, skip: int = 0, search: Optional[str] = ""):
    #cursor.execute(""" SELECT * FROM posts """)
    #posts = cursor.fetchall() 
    #print(posts)
    
    #This only returns all the posts related to a particular user 
    # and not every post in the database
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    # print(limit)

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(posts)
    return posts



@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #post_dict = post.dict()
    #post_dict['id'] = randrange(0, 1000000)
    #my_posts.append(post_dict)
    #cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #               (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    #print(**post.dict())
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # print(current_user.id)
    
    # print(current_user.email)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

 
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id= %s""", (id,))
    #retrieved_post = cursor.fetchone()
    
    #post = find_post(id)
    retrieved_post = db.query(models.Post).filter(models.Post.id == id).first()
    #print(retrieved_post)

    if not retrieved_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail = f"Post with id: {id} was not found")
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Post with id: {id} was not found"}
    
    #This only returns the posts which are made by a particular user and not any post of anyone
    # if retrieved_post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    #                         detail="Not authorized to perform requested action")
    
    return retrieved_post




@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (id,))
    #deleted_post = cursor.fetchone()
    #print(deleted_post)
    
    #index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                           detail= f"Post with id: {id} don't exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    #conn.commit()
    #my_posts.pop(index)
    #return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
     #              (post.title, post.content, post.published, id))
    #updated_post = cursor.fetchone()
    #conn.commit()

    # This only gives us the post query and if we use first(), then it returns us the first row
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    #print(updated_post)

    #index = find_index_post(id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Post with id: {id} don't exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    #ost_dict = post.dict()
    #post_dict["id"] = id
    #my_posts[index] = post_dict
    #return {"data": post_dict}
    #post_query.update({'title': 'Updated title', 'content': 'Updated content'}, synchronize_session=False)
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    #return updated_post
    return post_query.first()
