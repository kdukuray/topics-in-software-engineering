#main.py
#sqlite3
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from typing import ClassVar

app = FastAPI()

# Create tables if they don't already exist
models.Base.metadata.create_all(bind=engine)

# Dependency to get the DB session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Pydantic model for validating incoming data
#user
class User(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)  
    last_name: str = Field(min_length=1, max_length=100)



 

    USERS: ClassVar[list] = []

# Get all books from the database
'''
@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Books).all()
'''
#user
@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.User).all()


#create a new user
@app.post("/")
def create_user(user: User, db: Session = Depends(get_db)):
    user_model = models.User(
        first_name=user.first_name,
        last_name=user.last_name
    )

    db.add(user_model)
    db.commit()


'''
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    username: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.delete("/posts/{post_id}",status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db: db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Post was not found')
    db.delete(db_post)
    db.commit()

@app.post("/posts/",status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()


@app.get("/posts/{post_id}",status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        HTTPException(status_code=404,detail='Post was not found')
        return post

@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()


@app.get("/users/{user_id}",status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail='User not found')
    return user
    '''
