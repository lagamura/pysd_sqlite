# from xmlrpc.client import DateTime
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship
from database import Base
from datetime import datetime


class Simulation(Base):

    __tablename__ = "simulation"

    id = Column(Integer, primary_key=True)
    user: Column(String(30))
    model_name = Column(String(30), nullable=False)
    simulation_name = Column(String(30), nullable=False)
    csv_path = Column(String(50))
    timestamp = Column(String, default=datetime.now(tz=None).strftime("%Y_%m_%d-%H_%M_%S"))
    results =  Column(JSON)
    params = Column(JSON)

    def __repr__(self):
        return f"simulation_object_represantation(id={self.id!r}, simul_name={self.simulation_name!r}, csv_path={self.csv_path!r}, date={self.date!r})"

class ModelsNamespace(Base):

    __tablename__= "models"

    id_name = Column(String, primary_key=True)
    namespace = Column(JSON)
    docs = Column(JSON)

class Classroom(Base):
    __tablename__= "classroom"

    id_name = Column(String, primary_key=True)
    students = relationship("Student",back_populates="classroom")

class Student(Base):

    __tablename__= "student"
    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    surname = Column(String)
    department = Column(String)
    classroom_id = Column(String, ForeignKey("classroom.id_name"))
    classroom = relationship("Classroom", back_populates="students")
    email = Column(String)
    password = Column(String)


    

