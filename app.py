from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import JSON
import json

from sqlalchemy.orm import Session

import os
import crud, models, schema

from database import SessionLocal, engine

'''
import models
from database import engine

#this only needs on initialization
models.Base.metadata.create_all(bind=engine) ## This already exists in database.py probably should be deleted
'''
#models.Base.metadata.create_all(engine)

app = FastAPI(
    title = "Simulation_PySD_Manager",
    description = "Performe CRUD operations on csv files by using this API",
    version = "0.0.1",
    #root_path="/api" #this should be fixed
)

origins = [
"*"
]

allow_origin_regex = ['.*localhost.*',"http://localhost:3000/.*","https://pysims-frontend.herokuapp.com/.*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins = allow_origin_regex
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


@app.get('/get_available_models')
def get_available_models():
    # this should go to initalization
    '''
    with open('json_models.json', 'w') as outfile:
        json.dump(os.listdir('models'), outfile)
    '''
    try:
        models_list = os.listdir('models')
        return models_list
    except Exception as e:
        raise Exception(e)

@app.get('/get_all_csvs', response_model=list[schema.Simulation])
def get_all_csvs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    csv_list = crud.get_all_csvs(db=db, skip=skip, limit=limit)
    return csv_list

@app.get('/get_simuls', response_model= list[schema.Simulation])
def get_simuls(db: Session = Depends(get_db)):
    return crud.get_simuls(db)

@app.get('/get_simul_by_id/{id}', response_model= schema.Simulation)
def get_simul_by_id(id:int, db: Session = Depends(get_db)):
    obj = crud.get_simul_by_id(db=db, key_id=id)
    #input("Await------------------------\n")
    return(obj)

@app.get('/get_csv_by_id/{id}', response_class=FileResponse)
def get_csv_by_id(id:int, db: Session = Depends(get_db)):
    file_path = crud.get_simul_by_id(db=db, key_id=id).csv_path
    return FileResponse(file_path)

@app.get('/get_simul_res_json/{id}', response_class=JSONResponse)
def get_simul_res_json(id:int, db: Session = Depends(get_db)):
    row = crud.get_simul_by_id(db=db, key_id=id)
    content=json.loads(row.json_data) # this needs to be done because we are loading blob data from db
    return JSONResponse((content))


@app.get('/get_simul_by_name', response_model= schema.Simulation)
def get_simul_by_name(simul: schema.Get_Simul_by_name, db: Session = Depends(get_db)):
    return(crud.get_simul_by_name(db=db, model_details=simul.name))

@app.get('/get_csv_by_name', response_class= FileResponse, responses = {200: {"description": "returns a csv file." }})
def get_csv_by_name(simul: schema.Get_Simul_by_name, db: Session = Depends(get_db)):
    file_path = crud.get_csv_by_name(db=db, name_query=simul.name)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error" :"File not found!"}

@app.get('/get_model_namespace/{model_name}', response_class=JSONResponse)
def get_model_namespace(model_name:str, db: Session = Depends(get_db) ):
    return(crud.get_model_namespace(db=db, model_name=model_name))

@app.get('/get_model_docs/{model_name}', response_class=JSONResponse)
def get_model_docs(model_name:str, db: Session = Depends(get_db)):
    return(json.loads(crud.get_model_docs(db=db, model_name=model_name)))

@app.get('/get_csv_results', response_class=FileResponse)
def get_csv_results(db: Session = Depends(get_db)):
    file_path = crud.get_last_entry(db=db).csv_path
    return FileResponse(file_path, media_type="text/csv")

@app.get('/get_components_values/{model_name}')
def get_components_values(model_name:str):
    return(crud.get_components_values(model_name=model_name))

@app.post('/add_new_simulation/', response_model=schema.Simulation)
def add_new_simulation(simul: schema.Simul_post, step_run: bool=False,db: Session = Depends(get_db)):
    return (crud.run_simul(db=db, model_details=simul, step_run=step_run))

@app.post('/save_results', )
def save_results(simul: schema.Simul_post,db: Session = Depends(get_db)):
    return (crud.save_results(db=db, model_details=simul))

@app.delete('/delete_simul_by_id/{key_id}', response_description="deleted successfully")
def delete_simul_by_id(key_id:int, db: Session = Depends(get_db)):
    res = crud.get_simul_by_id(db=db, key_id=key_id)

    if not res:
        raise HTTPException(status_code=404, detail=f"No record found to delete")

    try:
        crud.delete_simul_by_id(db=db, key_id=key_id)
        fileDir = res.csv_path
        os.remove(fileDir)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to delete: {e}")
    return {"delete status": "success"}