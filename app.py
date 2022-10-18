from fastapi import Depends, FastAPI, HTTPException, status, Body
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import JSON, select, update
import json
import sys

from sqlalchemy.orm import Session

import os
import crud, models, schema

from database import SessionLocal, engine

from models import *


## Authentication
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

SECRET_KEY = "eacb3646506f975025d5d977eb225899c34a5bd28e97de7c17d4bb5b62561215"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

##
'''
from database import engine

#this only needs on initialization
models.Base.metadata.create_all(bind=engine) ## This already exists in database.py probably should be deleted
'''

app = FastAPI(
    title = "Simulation_PySD_Manager",
    description = "Performe CRUD operations on csv files by using this API",
    version = "0.0.1",
    #root_path="/api" #this should be fixed
)

#sys.setrecursionlimit(50)

origins = [
"*"
]

allow_origin_regex = ['.*localhost.*',"http://localhost:3000/.*","https://pysims-frontend.herokuapp.com/.*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
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
    return(obj)

@app.get('/get_csv_by_id/{id}', response_class=FileResponse)
def get_csv_by_id(id:int, db: Session = Depends(get_db)):
    file_path = crud.get_simul_by_id(db=db, key_id=id).csv_path
    return FileResponse(file_path)

@app.get('/get_simul_res_json/{id}', response_class=JSONResponse)
def get_simul_res_json(id:int, db: Session = Depends(get_db)):
    row = crud.get_simul_by_id(db=db, key_id=id)
    content=json.loads(row.results) # this needs to be done because we are loading blob data from db
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

@app.get('/get_vars_exposed/{model_name}', response_class=JSONResponse)
def get_vars_exposed(model_name:str, db: Session = Depends(get_db) ):
    q = db.query(ModelsNamespace).get(model_name.capitalize())
    return((q.vars_exposed))


@app.get('/get_model_docs/{model_name}', response_class=JSONResponse)
def get_model_docs(model_name:str, db: Session = Depends(get_db)):
    res = crud.get_model_docs(db=db, model_name=model_name)
    #print(res) #lets see...
    return(json.loads(res))

@app.get('/get_csv_results/{model_name}', response_class=FileResponse)
def get_csv_results(model_name: str):
    #file_path = crud.get_last_entry(db=db).csv_path #get from database

    file_path = crud.get_last_csv_filesys(model_name=model_name)

    return FileResponse(file_path, media_type="text/csv")

@app.get('/get_components_values/{model_name}')
def get_components_values(model_name:str):
    return(crud.get_components_values(model_name=model_name))

@app.get('/get_classrooms', response_class=JSONResponse)
def get_classrooms(db: Session = Depends(get_db)):

    classrooms = db.query(models.Classroom).all()

    return(classrooms)

@app.get('/get_students/{classroom_id}')
def get_students_classroom(classroom_id: str, db: Session = Depends(get_db)):

    res = db.query(models.Student).filter(models.Student.classroom_id == classroom_id).all()
    #print(res)
    return(res)

@app.get('/get_student/{id}')
def get_student(id: int):
    pass


@app.post('/add_new_simulation/')
def add_new_simulation(simul: schema.Simulation, step_run: bool=False,db: Session = Depends(get_db)):
    results = crud.run_simul(db=db, model_details=simul, step_run=step_run)
    return JSONResponse(results)

@app.post('/save_results' )
def save_results(simul: schema.Simulation,db: Session = Depends(get_db)):
    return (crud.save_results(db=db, model_details=simul))

@app.post('/add_classroom')
def add_classroom(classroom_name: str, db: Session = Depends(get_db)):
    crud.add_classroom(db=db,classroom_name=classroom_name )

@app.post('/add_student')
def add_student(student: schema.Student, db:Session= Depends(get_db)):
    _student = Student(**student.dict(exclude={'password'}))
    _student.password = get_password_hash(student.password)
    try:
        db.add(_student) 
        db.query(models.Classroom).filter(models.Classroom.id_name == _student.classroom_id).update({'num_students': models.Classroom.num_students + 1})
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to add Student {e}")
    return(_student)

@app.put('/update_password')
def update_password(password: str, db: Session = Depends(get_db)):
    pass

@app.delete('/delete_classroom')
def delete_classroom(classroom_name: str, db: Session = Depends(get_db)):
    #print(classroom_name)
    try:
        classroom = db.get(models.Classroom, classroom_name)
        #classroom = db.scalars(select(models.Classroom)).first()
        #print(classroom)
        db.delete(classroom)
        db.commit()
        db.flush()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to delete: {e}")

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

@app.delete('/delete_user/{key_id}', response_description="deleted successfully")
def delete_user(key_id: int, db: Session = Depends(get_db)):
    try:
        db.query(Student).filter(Student.id == key_id).delete()
        db.commit()

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to delete: {e}")
    return {"delete status": "success"}


# Auth

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)



def get_user(username: str, db: Session) -> Student:
    res = db.query(Student).filter(Student.username == username).first()
    if res:
        return (res)
    else :  raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


def authenticate_user(username: str, password: str, db: Session ):
    user = get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db ,username=token_data.username)
    if user is None:
        raise credentials_exception
    return user



@app.post("/token", response_model=schema.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),  db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "username": user.username}

@app.get("/users/me")
async def read_users_me(current_user: Student = Depends(get_current_user)):
    return current_user

@app.put("/update_vars_exposed/{model_name}")
def update_vars_exposed(model_name: str, vars_updated:dict = Body(), db: Session = Depends(get_db)):
    x = db.query(ModelsNamespace).get(model_name)
    # print(f"Vars Exposed: {vars_updated}")
    x.vars_exposed = vars_updated #update this
    db.commit()
    