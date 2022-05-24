from cgitb import text
from datetime import datetime
from pydantic import BaseModel, Json

class Simulation(BaseModel):
    id: int
    model_name: str
    simulation_name: str
    csv_path: str
    date: datetime
    json_data: Json

    class Config:
        orm_mode = True

class Simul_add(Simulation):
    pass

class Simul_test(BaseModel):
    model_name: str
    simulation_name: str

    class Config:
        orm_mode = True
         
class Get_Simul_by_name(BaseModel):
    simulation_name: str

    class Config:
        orm_mode = True

class Models(BaseModel):
    id_name: str
    namespace: Json