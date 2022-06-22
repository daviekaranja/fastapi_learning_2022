from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db : Session = Depends(database.get_db),
         current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {vote.post_id} does not exist')
    # checking from the database if the user has alredy liked the post
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id,
                                               models.Votes.user_id == current_user.id)
    already_voted = vote_query.first()
    if (vote.vote_direction == 1):
        # if the user has alredy liked the post raise a HTTP exception
        if already_voted:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'user {current_user.id} has already liked the post {vote.post_id}')

        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return f'post liked succesfuly'

    else:
        if not already_voted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='vote does not exist')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return 'liked removed'


