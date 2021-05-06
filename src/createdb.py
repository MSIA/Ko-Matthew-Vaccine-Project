import os
import sys
from config.flaskconfig import SQLALCHEMY_DATABASE_URI
import logging

import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData, Float, Text

import argparse

# set up logging config
logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

#argparse
parser = argparse.ArgumentParser(description="Create defined tables in database, for local or AWS database push")

args = parser.parse_args()

Base = declarative_base()

class vSentiment(Base):
    """Create a table used to store model parameters and features used to predict reasons why a person may not get the COVID-19 vaccine"""
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
        return '<vSentiment %r>' % self.id

def create_db():
    if os.environ.get('MYSQL_HOST') is None:
        logger.info("Database location: Local")
    else:
        logger.info("Database location: AWS RDS")
    # set up mysql connection
    engine = sql.create_engine(SQLALCHEMY_DATABASE_URI)

    # create the vaccine model table
    Base.metadata.create_all(engine)

    logger.info("Vaccine Sentiment Database created successfully!")
    
