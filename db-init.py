import pysd
import os
from os import path
import pathlib

from sqlalchemy.orm import   sessionmaker
from database import engine

import models

          
def database_init(db:sessionmaker):
    '''
    This script should be executed inside the src directory in order to work. Otherwise the values should be changed
    Probably, should be generalized for relative paths.
    '''

    #models.Base.metadata.create_all(engine)

    print("Initializing Database Models Table...")
    
    models_list = os.listdir('models')
    for model_name in models_list:
        fileDir = f'./models/{model_name}'

        if (not path.exists(fileDir)):
            raise Exception("There is not such a name model")

        fileExt = r'*.py'
        model_path = list(pathlib.Path(fileDir).glob(fileExt))        
        if (model_path):
            print(f'Model path .py is {model_path}')
            model = pysd.load(model_path[0])
        else:
            fileExt = r'*.mdl'
            model_path = list(pathlib.Path(fileDir).glob(fileExt))
            print(f'Model path .mdl is {model_path}')
            model = pysd.read_vensim(model_path[0])

        df = model.doc
        docs_json = df.to_json(orient = "index") # Orient Table Schema
        model_res = models.ModelsNamespace(id_name = model_name, namespace = model.namespace, docs = docs_json)

        try:
            instance = db.query(models.ModelsNamespace).filter_by(id_name=model_name).first()
            if instance:
                print(f"This Model already exists in db")
                continue
            db.add(model_res)
            db.commit()
            print("added into db successfully")
        except:
            # https://stackoverflow.com/questions/63556777/sqlalchemy-add-all-ignore-duplicate-key-integrityerror
            #db.rollback()
            raise Exception("Problem with adding in models table in database")
 
    return("Successfull Initialization")

def main():

    models.Base.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(engine)
    with SessionLocal() as session:
        database_init(session)
        #session.commit()


    

if __name__ == "__main__":
    main()
        