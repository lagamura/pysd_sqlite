from sqlalchemy import engine
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker




engine = create_engine("sqlite:///foo.db", future=True,connect_args={"check_same_thread": False}) #echo can be used for logging

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


Base.metadata.create_all(engine)


###### -------- watch out the correct order 1.declare base 2. engine creation 3.create all ######

def database_init():
    pass
       

''' #create new entry on db
with engine.begin() as connection:
    stocks.to_sql('mekokpesko', con=connection, if_exists='append') ### Warning about sqlconnection
'''