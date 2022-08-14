from sqlalchemy import engine
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
#from crud import database_init

SQLALCHEMY_DATABASE_URI = "sqlite:///./foo.db"

engine = create_engine(SQLALCHEMY_DATABASE_URI, future=True,connect_args={"check_same_thread": False}) #echo can be used for logging

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



#database_init(SessionLocal) # I am not sure this is correct

###### -------- watch out the correct order 1.declare base 2. engine creation 3.create all ######


    