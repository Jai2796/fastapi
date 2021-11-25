from fastapi import FastAPI, status, Response, Depends, HTTPException, APIRouter
from sqlalchemy.sql.expression import label, true
from sqlalchemy import func
from sqlalchemy.sql.functions import mode
from .. import models, schemas, oauth2
from typing import List, Optional
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(
        search)).limit(limit=limit).offset(offset=skip).all()

    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id,
                                                                                        isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit=limit).offset(offset=skip).all()
    print(posts)
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    return result


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def createposts(data: schemas.Postcreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # new_post = data.dict()
    # new_post['id'] = randrange(0, 100)
    # my_posts.append(new_post)
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (data.title, data.content, data.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **data.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def singlepost(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(id),)
    # post = cursor.fetchone()
    # post = find_post(id)
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            detail=f"post with id : {id} was not found", status_code=status.HTTP_404_NOT_FOUND)
    return post


@router.delete("/{id}")
def deletepost(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    delete = delete_post.first()

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", str(id))
    # delete_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    if delete == None:
        raise HTTPException(
            detail=f"post with id:{id} does not exits", status_code=status.HTTP_404_NOT_FOUND)
    if delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    delete_post.delete(synchronize_session=False)
    db.commit()
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def updateposts(id: int, post: schemas.Postcreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    updated = updated_post.first()

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    if updated == None:
        raise HTTPException(
            detail=f"post with id:{id} does not exits", status_code=status.HTTP_404_NOT_FOUND)
    if updated.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    # new_post = post.dict()
    # new_post['id'] = id
    # my_posts[index] = new_post
    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()
