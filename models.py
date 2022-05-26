# from xmlrpc.client import DateTime
from sqlalchemy import Column, Integer, String, JSON, DateTime
from database import Base, SessionLocal
from datetime import datetime

class Simulation(Base):

    __tablename__ = "Simulation"

    id = Column(Integer, primary_key=True)
    model_name = Column(String(30), nullable=False)
    simulation_name = Column(String(30), nullable=False)
    csv_path = Column(String(50))
    date = Column(DateTime, default=datetime.utcnow)
    json_data =  Column(JSON)

    def __repr__(self):
        return f"simulation_object_represantation(id={self.id!r}, simul_name={self.simulation_name!r}, csv_path={self.csv_path!r}, date={self.date!r})"

class ModelsNamespace(Base):

    __tablename__= "Models"

    id_name = Column(String, primary_key=True)
    namespace = Column(JSON)
    docs = Column(JSON)



