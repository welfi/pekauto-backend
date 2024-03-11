from sqlalchemy import Column, Integer, Enum, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from django.conf import settings

Base = declarative_base()


class VIN(Base):
    __tablename__ = 'vin'

    id = Column(Integer, primary_key=True)
    version = Column(String)
    equipment_code = Column(Enum('000', '014', '037', '036', '038', '027'))
    year_of_issue = Column(String)
    serial_number = Column(Integer)
    place_of_production = Column(Enum('00', '01'))

