from sqlalchemy import Column, Integer, String, JSON
from database import Base

class Simulation(Base):

    __tablename__ = "simul_csv"

    id = Column(Integer, primary_key=True)
    model_name = Column(String(30))
    simulation_name = Column(String(30))
    csv_path = Column(String(50))
    date = Column(String(30))
    json_data =  Column(JSON)

    def __repr__(self):
        return f"simulation_object_represantation(id={self.id!r}, simul_name={self.simulation_name!r}, csv_path={self.csv_path!r}, date={self.date!r})"

