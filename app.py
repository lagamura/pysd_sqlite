from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import JSON, select
import json
import sys

from sqlalchemy.orm import Session

import os
import crud, models, schema

from database import SessionLocal, engine

from models import Student


## Authentication
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext

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

@app.get('/get_model_docs/{model_name}', response_class=JSONResponse)
def get_model_docs(model_name:str, db: Session = Depends(get_db)):
    return(json.loads(crud.get_model_docs(db=db, model_name=model_name)))

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
    _student = Student(**student.dict())
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
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user



@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db) ):
    user_dict = db.query(Student).filter(Student.username == form_data.username).first()
    print(user_dict.password)    
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    print(hashed_password)
    if not hashed_password == user_dict.password:
        print("Exception in hashed_password")
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user_dict.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: Student = Depends(get_current_user)):
    return current_user
