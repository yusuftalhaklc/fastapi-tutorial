from typing import Optional, List
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(
            host="localhost", 
            database="fastapi", 
            user="postgres", 
            password="admin",
            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection was succesfull")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error : ",error)
        time.sleep(2)

app.include_router(post.routes)
app.include_router(user.routes)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message":"Welcome to my api"}