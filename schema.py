from cgitb import text
from datetime import datetime
import json
from pydantic import BaseModel, Json
from typing import(Optional)

class Simulation(BaseModel):
    id: int
    model_name: str
    simulation_name: str
    csv_path: str
    date: datetime
    json_data: Json
    params: dict | None

    class Config:
        orm_mode = True

class Simul_post(BaseModel):
    user: str
    timestamp: datetime
    model_name: str
    simulation_name: str
    params: dict | None #this is an object of key-value pairs. Maybe should be changed

    class Config:
        orm_mode = True

class Models_init(BaseModel):
    id_name: str
    namespace: Json
    docs: Json
         
class Get_Simul_by_name(BaseModel):
    simulation_name: str

    class Config:
        orm_mode = True

class Models(BaseModel):
    id_name: str
    namespace: Json
