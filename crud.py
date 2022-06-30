import pysd
import pandas as pd
import json

from datetime import datetime
import pathlib
import os
from os import path

from database import engine
from sqlalchemy.orm import Session

import models
import schema

def database_init(db:Session):
    
    models_list = os.listdir('models')
    for model_name in models_list:

        fileDir = f'./models/{model_name}'

        if (not path.exists(fileDir)):
            raise Exception("There is not such a name model")

        fileExt = r'*.py'
        model_path = list(pathlib.Path(fileDir).glob(fileExt))        
        #print (model_path)
        if (model_path):
            model = pysd.load(model_path[0])
        else:
            fileExt = r'*.mdl'
            model_path = list(pathlib.Path(fileDir).glob(fileExt))
            model = pysd.read_vensim(model_path)
        model_res = models.ModelsNamespace(id_name = model_name, namespace = model.namespace)
        db.add(model_res) 

        db.commit()
        
    return("Successfull Initialization")
        

def get_simuls(db:Session):
    res = db.query(models.Simulation).all()
    return res

def get_simul_by_name(db:Session, name_query: str):
    return db.query(models.Simulation).filter(models.Simulation.model_name == name_query).first()
    
def get_simul_by_id(db:Session, key_id:int ):
    return db.query(models.Simulation).filter(models.Simulation.id == key_id).first()


def post_simul(db:Session, model_details: schema.Simul_post):
    fileDir = f'./models/{model_details.model_name}'

    if (not path.exists(fileDir)):
        raise Exception("There is not such a name model")

    fileExt = r'*.py'
    model_path = list(pathlib.Path(fileDir).glob(fileExt))        
    #print (model_path)
    if (model_path):
        model = pysd.load(model_path[0])
    else:
        fileExt = r'*.mdl'
        model_path = list(pathlib.Path(fileDir).glob(fileExt))
        model = pysd.read_vensim(model_path)


    if (model_details.params is None):
        df = model.run()
    else:
        print(model_details.params)
        #model_details.params = "{\"room_temperature\":20}"
        df = model.run(params=json.loads(model_details.params))

    result = df.to_json(orient="columns") # json.load() removed. creation of json_field stored in sqlite3
    
    os.makedirs(f'./user/results/{model_details.model_name}', exist_ok=True)
    #print(getListOfMdls(os.path.join(os.curdir,'models')))
    csv_path = f'./user/results/{model_details.model_name}/{datetime.now(tz=None).strftime("%Y_%m_%d-%H_%M_%S")}.csv'
    df.to_csv(csv_path)
    # create db entry
    
    simulation_res = models.Simulation(simulation_name= model_details.simulation_name, model_name = model_details.model_name, csv_path = csv_path, json_data = result )
    db.add(simulation_res) 

    db.commit()
    print(f'Id is: {simulation_res.id}')

    return(simulation_res)

### WARNING THIS FUNCTION HAS NOT SCHEMA MODEL ###
def get_csv_by_id(db:Session, id_query:int):
    with db(engine) as session:

        res = session.query(models.Simulation).get(id_query)
        pd_fetched = pd.read_csv(res.csv_path)
    
    return(pd_fetched)


### WARNING THIS FUNCTION HAS NOT SCHEMA MODEL ###
def get_csv_by_name(db:Session, name_query:str):

    res = db.query(models.Simulation).get(name_query)
    if res:
        #pd_fetched = pd.read_csv(res.csv_path)
        return(res.csv_path)
    else:
        return("There is no such filename - something went wrong")


def get_all_csvs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Simulation).offset(skip).limit(limit).all()

def get_model_namespace(db: Session, model_name:str):
    try:
        res = db.query(models.ModelsNamespace).get(model_name)
        if res:
            return(res.namespace)
    except Exception as e:
        raise Exception(e)

def get_model_docs(db: Session, model_name:str):
    try:
        res = db.query(models.ModelsNamespace).get(model_name)
        if res:
            return(res.docs)
    except Exception as e:
        raise Exception(e)

def delete_simul_by_id(db: Session, key_id:int):
    try:
        db.query(models.Simulation).filter(models.Simulation.id == key_id).delete()
        db.commit()
    except Exception as e:
        raise Exception(e)

def clear_models_table(db: Session):
        try:
            db.query(models.ModelsNamespace).delete()
            db.commit()
        except Exception as e:
            raise Exception(e)

        