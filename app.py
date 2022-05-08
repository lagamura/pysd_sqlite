from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

import os
import crud
import models
import schema
from database import SessionLocal, engine




models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "Simulation_PySD_Manager",
    description = "Performe CRUD operations on csv files by using this API",
    version = "0.0.1"
)

origins = [
"*"
]

allow_origin_regex = ['.*localhost.*',"http://localhost:3000/.*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
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

@app.get('/get_all_csvs', response_model=list[schema.Simulcsv_Base])
def get_all_csvs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    csv_list = crud.get_all_csvs(db=db, skip=skip, limit=limit)
    return csv_list

@app.get('/get_simuls', response_model= list[schema.Simulcsv_Base])
def get_simuls(db: Session = Depends(get_db)):
    return crud.get_simuls(db)

@app.get('/get_simul_by_id/{id}', response_model= schema.Simulcsv_Base)
def get_simul_by_id(id:int, db: Session = Depends(get_db)):
    obj = crud.get_simul_by_id(db=db, key_id=id)
    #input("Await------------------------\n")
    return(obj)

@app.get('/get_csv_by_id/{id}', response_class=FileResponse)
def get_csv_by_id(id:int, db: Session = Depends(get_db)):
    file_path = crud.get_simul_by_id(db=db, key_id=id).csv_path
    return FileResponse(file_path)

@app.get('/get_simul_res_json/{id}')
def get_simul_res_json(id:int, db: Session = Depends(get_db)):
    row = crud.get_simul_by_id(db=db, key_id=id)
    return(row.json_data)


@app.get('/get_simul_by_name', response_model= schema.Simulcsv_Base)
def get_simul_by_name(simul: schema.Get_Simul_by_name, db: Session = Depends(get_db)):
    return(crud.get_simul_by_name(db=db, model_details=simul.name))

@app.get('/get_csv_by_name', response_class= FileResponse, responses = {200: {"description": "returns a csv file." }})
def get_csv_by_name(simul: schema.Get_Simul_by_name, db: Session = Depends(get_db)):
    file_path = crud.get_csv_by_name(db=db, name_query=simul.name)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error" :"File not found!"}


@app.post('/add_new_csv', response_model=schema.Simulcsv_Base)
def add_new_csv(simul: schema.Simul_test, db: Session = Depends(get_db)):
    return (crud.post_simul_csv(db=db, model_details=simul))

@app.delete('/delete_csv_by_id', response_description="deleted successfully")
def delete_csv_by_id(key_id:int, db: Session = Depends(get_db)):
    res = crud.get_simul_by_id(db=db, key_id=key_id)


    if not res:
        raise HTTPException(status_code=404, detail=f"No record found to delete")

    try:
        crud.delete_csv_by_id(db=db, key_id=key_id)
        fileDir = res.csv_path
        os.remove(fileDir)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to delete: {e}")
    return {"delete status": "success"}