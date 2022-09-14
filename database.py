from sqlalchemy import engine
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
#from crud import database_init

SQLALCHEMY_DATABASE_URI = "sqlite:///./foo.db"
#SQLALCHEMY_DATABASE_URI = "postgresql://user:password@postgresserver/db"
#SQLALCHEMY_DATABASE_URI = "postgresql://zkfhojomydbtyj:126966877ba800983dc6fcfd7557e625a35c01496c17e2f794c77a21119b64d0@ec2-54-228-218-84.eu-west-1.compute.amazonaws.com:5432/d59046ahv6dkcm"

#check same thread: false is used only for sqlite locally
engine = create_engine(SQLALCHEMY_DATABASE_URI, future=True, connect_args={"check_same_thread":False}) #echo can be used for logging

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



#database_init(SessionLocal) # I am not sure this is correct

###### -------- watch out the correct order 1.declare base 2. engine creation 3.create all ######


    