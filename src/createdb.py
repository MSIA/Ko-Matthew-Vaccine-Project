import logging.config
import os

import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float
from config.flaskconfig import SQLALCHEMY_DATABASE_URI

logger = logging.getLogger(__name__)

Base = declarative_base()

class VaccineSentiment(Base):
    '''Create a table used to store model parameters for application use'''
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
    '''Create the database and tables either locally or in AWS RDS'''
    if os.environ.get('MYSQL_HOST') is None:
        logger.info('Database location: Local')
        logger.debug('Set MYSQL_HOST variable for AWS RDS instead of local')
    else:
        logger.info('Database location: AWS RDS')
        logger.debug('Remove MYSQL_HOST variable for local instead of AWS')
    # set up mysql connection
    engine = sql.create_engine(SQLALCHEMY_DATABASE_URI)

    try:
        Base.metadata.create_all(engine)
    except sql.exc.OperationalError:
        logger.error('Unable to create database')
        logger.warning('Please connect to Northwestern VPN or campus WiFi,\
                        or remove MY_SQL env variable for local location')
    else:
        logger.info('Vaccine Sentiment Database created successfully.')
