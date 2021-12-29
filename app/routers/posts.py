from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func


router = APIRouter(
    prefix='/posts',
    tags=['Posts'],
)


@router.get('/',  response_model=List[schemas.PostwVotes])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    # cursor.execute("""SELECT * FROM public."Posts"
    # ORDER BY id ASC """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse,)
# post: Post):
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):
    # cursor.execute("""INSERT INTO public."Posts" (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title, post.content, post.published))

    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=schemas.PostwVotes)
def get_post(id: int, db: Session = Depends(get_db)):  # response: Response):
    # cursor.execute("""SELECT * FROM public."Posts" WHERE id=%s""",
    #                (str(id),))  # Add comma at end for avoiding errors
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == id).first()
    if not results:  # used to be post inplace of results
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id {id} not found"}
    return results


@router.delete('/{id}')
def delete_post(id: int, response: Response, status_code=status.HTTP_204_NO_CONTENT, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):
    # cursor.execute(
    #     """DELETE FROM public."Posts" WHERE id=%s RETURNING *""", (str(id),))
    # del_post = cursor.fetchone()

    del_post_query = db.query(models.Post).filter(models.Post.id == id)
    del_post = del_post_query.first()
    if del_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    if del_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=('Not authorized to perform requested action'))
    # conn.commit()
    del_post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):
    # cursor.execute("""UPDATE public."Posts" SET title=%s,content=%s,published=%s WHERE id=%s RETURNING * """,
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    upd_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = upd_post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=('Not authorized to perform requested action'))
    # conn.commit()
    upd_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post
