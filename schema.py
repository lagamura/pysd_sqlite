from datetime import datetime
from pydantic import BaseModel

class Simulcsv_Base(BaseModel):
    id: int
    name: str
    csv_path: str
    date: datetime

    class Config:
        orm_mode = True

class Simulcsv_add(Simulcsv_Base):
    pass

class Simul_test(BaseModel):
    id: int
    model_name: str

    class Config:
        orm_mode = True
         
class Get_Simul_by_name(BaseModel):
    name: str

    class Config:
        orm_mode = True
