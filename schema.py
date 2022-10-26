from cgitb import text
from datetime import datetime
import json
import numbers
from pydantic import BaseModel, Json, EmailStr, SecretStr
from typing import(Optional)
from enum import Enum

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

class AdminEnum(str, Enum):
    user_access="user_access"
    admin_access="admin_access"

class Student(BaseModel):

    id: int
    firstname: str
    surname: str
    department: str
    classroom_id: str
    username : str
    password: str
    email : EmailStr 
    access_level : AdminEnum | None

    class Config:
        schema_extra = {
            "example": {
                "id": 1828,
                "firstname": "Stelios",
                "surname": "Lagaras",
                "department": "e-ce",
                "classroom_id": "ECE_101",
                "username": "slagaras",
                "email": "stelioslagaras@gmail.com",
                "password": "secret", #ayto mallon skai bug
                "access_level": AdminEnum.user_access
            }
        }
        orm_mode = True
        

         
class Get_Simul_by_name(BaseModel):
    simulation_name: str

    class Config:
        orm_mode = True

class Models(BaseModel):
    id_name: str
    namespace: Json
    

## Authentication part

# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None


# class UserInDB(User):
#     hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

class TokenData(BaseModel):
    username: str | None = None
