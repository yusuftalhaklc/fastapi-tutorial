from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/fastapi'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost", 
#             database="fastapi", 
#             user="postgres", 
#             password="admin",
#             cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("database connection was succesfull")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error : ",error)
#         time.sleep(2)