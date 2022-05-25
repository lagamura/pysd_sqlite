import pysd
import os
import os
from os import path
import pathlib

import models
from database import engine
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi import Depends



def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()  
          
def database_init(db:Session):

    print("Initializing Database Models Table...")
    
    models_list = os.listdir('models')
    for model_name in models_list:
        model_name = "Teacup"
        fileDir = f'./models/{model_name}'

        if (not path.exists(fileDir)):
            raise Exception("There is not such a name model")

        fileExt = r'*.py'
        model_path = list(pathlib.Path(fileDir).glob(fileExt))        
        print(model_path)
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

def main():
    database_init(Depends(get_db))


    

if __name__ == "__main__":
    main()
        