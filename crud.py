import pysd
import pandas as pd

from datetime import datetime
import pathlib
import os
from os import path

from database import engine
from sqlalchemy.orm import Session

import models
import schema

def get_simuls(db:Session):
    #return models.Simul_csv.query.all()
    res = db.query(models.Simul_csv).all()
    return res

def get_simul_by_name(db:Session, name_query: str):
    return db.query(models.Simul_csv).filter(models.Simul_csv.model_name == name_query).first()
    
def get_simul_by_id(db:Session, key_id:int ):
    return db.query(models.Simul_csv).filter(models.Simul_csv.id == key_id).first()


def post_simul_csv(db:Session, model_details: schema.Simul_test):
    #user_choice = input("Type the model you want to execute: ")
    fileDir = f'./models/{model_details.model_name}'
    fileExt = r'*.py'
    model_path = list(pathlib.Path(fileDir).glob(fileExt))

    if (not path.exists(fileDir)):
        raise Exception("There is not such a name model")

    model = pysd.load(model_path[0])
    df = model.run()
    
    os.makedirs(f'./user/results/{model_details.model_name}', exist_ok=True)
    #print(getListOfMdls(os.path.join(os.curdir,'models')))
    csv_path = f'./user/results/{model_details.model_name}/{datetime.now(tz=None).strftime("%Y_%m_%d-%H_%M_%S")}.csv'
    df.to_csv(csv_path)
    datetime_field = datetime.now(tz=None).strftime("%Y-%m-%dT%H:%M:%S")
    # create db entry

    simulation_res_csv = models.Simul_csv(name = model_details.model_name, csv_path = csv_path, date = datetime_field)
    db.add(simulation_res_csv)
    db.commit()
    print(f'Id is: {simulation_res_csv.id}')

    return(simulation_res_csv)

### WARNING THIS FUNCTION HAS NOT SCHEMA MODEL ###
def get_csv_by_id(db:Session, id_query:int):
    with db(engine) as session:

        res = session.query(models.Simul_csv).get(id_query)
        pd_fetched = pd.read_csv(res.csv_path)
    
    return(pd_fetched)


### WARNING THIS FUNCTION HAS NOT SCHEMA MODEL ###
def get_csv_by_name(db:Session, name_query:str):
    with db(engine) as session:

        res = session.query(models.Simul_csv).get(name_query)
        if res:
            #pd_fetched = pd.read_csv(res.csv_path)
            return(res.csv_path)
        else:
            return("There is no such filename - something went wrong")


def get_all_csvs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Simul_csv).offset(skip).limit(limit).all()

def delete_csv_by_id(db: Session, key_id:int):

    try:
        db.query(models.Simul_csv).filter(models.Simul_csv.id == key_id).delete()
        db.commit()
    except Exception as e:
        raise Exception(e)

'''
def get_all_models(db: Session):
    return(os.listdir('/models'))

'''
        