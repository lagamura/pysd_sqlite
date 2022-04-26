from logging import raiseExceptions
from unittest import result
import pysd
import pandas as pd
from sqlalchemy import Table, Column, Integer, String, MetaData, LargeBinary, engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import registry
from sqlalchemy.orm import aliased
from sqlalchemy import select
import os
from functions import getListOfMdls
from datetime import datetime
import pathlib

# engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True) #echo can be used for logging
Base = declarative_base()
engine = create_engine("sqlite:///foo.db", echo=True, future=True) #echo can be used for logging


class Simul_csv(Base):

    __tablename__ = "simul_csv"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    csv_path = Column(String(50))

    def __repr__(self):
        return f"simul_id(id={self.id!r}, simul_name={self.name!r})"

Base.metadata.create_all(engine)


###### ------------------------------------- watch out the correct order 1.declare base 2. engine creation 3.create all ######

def database_init():
    pass
       

def post_simul_csv():
    #user_choice = input("Type the model you want to execute: ")
    user_choice = "Teacup"
    fileDir = f'./models/{user_choice}'
    fileExt = r'*.py'
    model_path = list(pathlib.Path(fileDir).glob(fileExt))

    if (model_path == None):
        raise Exception("There is not such a name model")

    model = pysd.load(model_path[0])
    df = model.run()

    os.makedirs(f'./user/results/{user_choice}', exist_ok=True)
    #print(getListOfMdls(os.path.join(os.curdir,'models')))
    csv_path = f'./user/results/{user_choice}/{datetime.now(tz=None).strftime("%Y_%m_%d-%H_%M_%S")}.csv'
    df.to_csv(csv_path)

    # create db entry

    with Session(engine) as session:

        simulation_res_csv = Simul_csv(name = user_choice, csv_path = csv_path)
        session.add(simulation_res_csv)
        session.commit()
        print(f'Id is: {simulation_res_csv.id}')



    return("successfully saved a csv_filepath in our database")


def get_csv(id_query:int):
    with Session(engine) as session:

        res = session.query(Simul_csv).get(id_query)
        pd_fetched = pd.read_csv(res.csv_path)
    
    return(pd_fetched)





def main():
    database_init()
    # post_simul_csv()
    get_csv(1)
    
    print("------------\n")

    ###-----###



if __name__ == "__main__":
    main()




''' #create new entry on db
with engine.begin() as connection:
    stocks.to_sql('mekokpesko', con=connection, if_exists='append') ### Warning about sqlconnection
'''