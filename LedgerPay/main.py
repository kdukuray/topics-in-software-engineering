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
    first_name: str = Field(min_length=1)  
    last_name: str = Field(min_length=1, max_length=100)



   

    USERS: ClassVar[list] = []

# Get all books from the database

#user
@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.post("/")
def create_user(user: User, db: Session = Depends(get_db)):
    # Correct way to instantiate a SQLAlchemy model
    user_model = models.User(
        first_name=user.first_name,
        last_name=user.last_name
    )

    # Add the user model to the session and commit it
    db.add(user_model)
    db.commit()  # Commit the transaction

    # Return the created user or a success message
    return user


# Update user information
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} : Does not exist"
        )

    # Update the user's attributes
    user_model.first_name = user.first_name
    user_model.last_name = user.last_name

    db.commit()

    # Return the updated user model
    return user_model


# Delete a user from the database
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} : Does not exist"
        )

    db.delete(user_model)
    db.commit()

    return {"detail": f"User with ID {user_id} has been deleted."}
