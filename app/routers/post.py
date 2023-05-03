from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends , APIRouter
from .. import models,schemas, oauth2
from sqlalchemy.orm import Session
from ..database import engine, get_db


routes = APIRouter(
    prefix= "/posts" ,
    tags= ['Posts']
)

@routes.get("/",response_model=List[schemas.PostResponse])
def posts(
    db: Session = Depends(get_db),
    current_user:int = Depends(oauth2.get_current_user),
    limit:int = 10):
    
    posts = db.query(models.Post).limit(limit).all()

    return posts

@routes.post("/",status_code = status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), 
                current_user:int = Depends(oauth2.get_current_user)):


    new_post = models.Post(owner_id=current_user.id, **post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
 
@routes.get("/latest")
def get_latest_post():
    return {"post_detail": "post" }

@routes.get("/{id}", response_model=schemas.PostResponse)
def get_post(id : int, 
             db: Session = Depends(get_db), 
             current_user:int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    return post 

@routes.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, 
                db: Session = Depends(get_db), 
                current_user:int = Depends(oauth2.get_current_user)):
    deleted_posts_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_posts = deleted_posts_query.first()


    if deleted_posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    if deleted_posts.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    deleted_posts_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@routes.put("/{id}", response_model=schemas.PostResponse)
def update_post(id:int, 
                post:schemas.PostCreate, 
                db: Session = Depends(get_db),
                current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id) 

    post_updated = post_query.first()

    if post_updated == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    if posts.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    post_query.update(post.dict() ,synchronize_session=False)
    db.commit()

    return post_query.first()