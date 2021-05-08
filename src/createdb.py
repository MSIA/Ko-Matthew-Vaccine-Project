import logging.config

import os
import sqlalchemy as sql
from config.flaskconfig import SQLALCHEMY_DATABASE_URI
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float

logger = logging.getLogger(__name__)

Base = declarative_base()

class VaccineSentiment(Base):
    """Create a table used to store model parameters for application use"""
    __tablename__ = 'vaccine_model'
    id = Column(Integer, primary_key=True)
    female = Column(Float, unique=False, nullable=True)
    race = Column(Float, unique=False, nullable=True)
    education = Column(Float, unique=False, nullable=True)
    marital_status = Column(Float, unique=False, nullable=True)
    where_work = Column(Float, unique=False, nullable=True)
    work_from_home = Column(Float, unique=False, nullable=True)
    region = Column(Float, unique=False, nullable=True)
    age = Column(Float, unique=False, nullable=True)

    def __repr__(self):
        return '<VaccineSentiment %r>' % self.id

def create_db():
    """Create the database and tables either locally or in AWS RDS"""
    if os.environ.get('MYSQL_HOST') is None:
        logger.info("Database location: Local")
    else:
        logger.info("Database location: AWS RDS")
    # set up mysql connection
    engine = sql.create_engine(SQLALCHEMY_DATABASE_URI)
    # create the vaccine_model table
    Base.metadata.create_all(engine)
    logger.info("Vaccine Sentiment Database created successfully.")
