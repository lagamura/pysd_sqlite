from cgitb import text
from datetime import datetime
import json
import numbers
from pydantic import BaseModel, Json, EmailStr, SecretStr
from typing import(Optional)

class Simulation(BaseModel):
    id: int | None
    model_name: str
    simulation_name: str | None
    csv_path: str | None
    timestamp: str | None
    user: str | None
    params: Json | dict | None #this should be specified
    results: Json | dict | None
    end_time: float | None
    start_time: float | None

    class Config:
        orm_mode = True



    class Config:
        orm_mode = True


# class Simul_post(BaseModel):
#     user: str
#     timestamp: datetime
#     model_name: str
#     simulation_name: str | None
#     params: dict | None #this is an object of key-value pairs. Maybe should be changed
#     start_time: float
#     end_time: float
#     class Config:
#         orm_mode = True

class Student(BaseModel):

    id: int
    firstname: str
    surname: str
    department: str
    classroom_id: str
    email : EmailStr 
    password : str | None

    class Config:
        schema_extra = {
            "example": {
                "id": 1828,
                "firstname": "Stelios",
                "surname": "Lagaras",
                "department": "e-ce",
                "classroom_id": "ECE_101",
                "email": "stelioslagaras@gmail.com",
                "password": "hiddentypepass"
            }
        }
        

         
class Get_Simul_by_name(BaseModel):
    simulation_name: str

    class Config:
        orm_mode = True

class Models(BaseModel):
    id_name: str
    namespace: Json
