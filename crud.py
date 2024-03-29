import pysd
import pandas as pd
import json

from datetime import datetime
import pathlib
import os
from os import path
import glob

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

def get_last_entry(db:Session):
    return db.query(models.Simulation).order_by(models.Simulation.id.desc()).first()

def get_last_csv_filesys(model_name: str):

    os.makedirs(f'./user/results/{model_name}', exist_ok=True)
    #print(getListOfMdls(os.path.join(os.curdir,'models')))
    folder_path = f'./user/results/{model_name}'
    file_type = r'\*csv'
    files = glob.glob(folder_path + file_type)
    max_file = max(files, key=os.path.getctime)
    return(max_file)

def run_simul(db:Session, model_details: schema.Simulation, step_run: bool):

    fileDir = f'./models/{model_details.model_name}'

    if (not path.exists(fileDir)):
        raise Exception("There is not such a name model")

    fileExt = r'*.py'
    model_path = list(pathlib.Path(fileDir).glob(fileExt))        
    if (model_path):
        model = pysd.load(model_path[0])
    else:
        fileExt = r'*.mdl'
        model_path = list(pathlib.Path(fileDir).glob(fileExt))
        model = pysd.read_vensim(model_path)

     #cur_step as an integer - (0...1..2...N)
    
    cur_step = int((model_details.end_time - model["INITIAL TIME"] - model["TIME STEP"])/model["TIME STEP"])

    print(f'cur_step is:{cur_step}')
    
    # Here starts the model run part
    if (step_run):
        if(cur_step > 0): #path.exists("./user/results/pickles/final_state.pic")
            print(f'N_th run of Simulation:({model_details.start_time}, {model_details.end_time})')
            df = model.run(initial_condition="./user/results/pickles/final_state.pic", return_timestamps=(model_details.start_time, model_details.end_time),params=(model_details.params))

        else:
            print(f'1st Run of Simulation:({model["INITIAL TIME"]},{model["TIME STEP"]})')
            df = model.run(params=(model_details.params),return_timestamps=(model["INITIAL TIME"],model["TIME STEP"]))
            #print(df)
  
    else:
        print(f'model_details params are: {model_details.params}')
        if(cur_step>0): #cur_step > 0
            df = model.run(initial_condition="./user/results/pickles/final_state.pic", params=(model_details.params))
        else:
            df = model.run(params=(model_details.params))

    # Output Part
    os.makedirs(f'./user/results/pickles/', exist_ok=True)
    model.export("./user/results/pickles/final_state.pic")

    if(cur_step>0):
        data_as_dict = df.to_dict() # storing for merging in step run
        f = open(f'./user/results/simulation_state.json')
        dict_before = json.load(f)
        result = mergeStepDicts(dict_before,data_as_dict)
    else:
        data_as_dict = df.to_dict() # storing for merging in step run
        result = data_as_dict


    #result = (df.to_json(orient="columns")) # sending from API data
    with open(f'./user/results/simulation_state.json', 'w') as convert_file:
        convert_file.write(json.dumps(result))

        # create db entry


    print(f'cur_step={cur_step}')

    save_csv_simulation(model_details) # save csv simulation in filesystem


    #results = json.dumps(result)
    #print (results)

    return(result)

def save_results(db:Session, model_details: schema.Simulation):

    os.makedirs(f'./user/results/{model_details.model_name}', exist_ok=True)
    #print(getListOfMdls(os.path.join(os.curdir,'models')))
    csv_path = f'./user/results/{model_details.model_name}/{datetime.now(tz=None).strftime("%Y_%m_%d-%H_%M_%S")}.csv'
    
    try:
        f = open(f'./user/results/simulation_state.json')
    except Exception as e:
        raise Exception(e)

    df = pd.read_json(f, orient='columns')
    df.to_csv(csv_path)
    ### END ###

    f = open(f'./user/results/simulation_state.json')
    dict_res = json.load(f) ### BUUGGGGGGG WITH SOME DUPLICATE KEYS ON MERGING
    result  = dict_res   

    simulation_res = models.Simulation(simulation_name= model_details.simulation_name,
    model_name = model_details.model_name, 
    csv_path = csv_path,
    results = (result),
    params = model_details.params,
    timestamp = datetime.now(tz=None).strftime("%Y_%m_%d-%H_%M_%S")
    )

    db.add(simulation_res) 
    db.commit()
    print(f'Id is: {simulation_res.id}')
    
    return(True)


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
    return db.query(models.Simulation).offset(skip).limit(limit).all() #Does this work?

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

def get_components_values(model_name:str): #test to avoid using db
    
    results_dict = {}
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

    for component_name in model.doc["Real Name"]:
        results_dict.update({component_name: model[component_name]})
        
    #print(results_dict)

    return(results_dict)

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

def add_classroom(db: Session, classroom_name:str):
    try:
        db.add(models.Classroom(id_name = classroom_name, num_students = 0 )) 
        db.commit()
    except Exception as e:
        raise Exception(e)

### HELPOUT functions ###

def mergeStepDicts(dict_1, dict_2):
    dict_3={}
    for dict_comp in dict_1:
        dict_3[dict_comp] = {**dict_1[dict_comp] , **dict_2[dict_comp]}
    return dict_3

def save_csv_simulation(model_details):
    os.makedirs(f'./user/results/{model_details.model_name}', exist_ok=True)
    #print(getListOfMdls(os.path.join(os.curdir,'models')))
    csv_path = f'./user/results/{model_details.model_name}/{datetime.now(tz=None).strftime("%Y_%m_%d-%H_%M_%S")}.csv'
    
    try:
        f = open(f'./user/results/simulation_state.json')
    except Exception as e:
        raise Exception(e)

    df = pd.read_json(f, orient='columns')
    df.to_csv(csv_path)
    ### END ###       