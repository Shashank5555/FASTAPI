from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#         password='1447459', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:12345@localhost/default'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = DeclarativeBase()

#This creates a session of the database which is connected above each time
# an API request is made. 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
