import logging.config
import os

import pandas as pd
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from config.flaskconfig import SQLALCHEMY_DATABASE_URI

logger = logging.getLogger(__name__)

Base = declarative_base()


class VaccineSentiment(Base):
    '''Create a table used to store clean data for application use'''
    __tablename__ = 'vaccine_response'
    output = Column(Integer, unique=False, nullable=True)
    url = Column(String(200), unique=False, nullable=True)
    response = Column(String(500), unique=False, nullable=True)
    reason = Column(String(100), unique=False, nullable=True)
    id = Column(Integer, primary_key=True)

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
        logger.info("Database created from %s", SQLALCHEMY_DATABASE_URI)
    except sql.exc.OperationalError:
        logger.error('Unable to create database')
        logger.warning('Please connect to Northwestern VPN or campus WiFi,\
                        or remove MY_SQL env variable for local location')
    else:
        logger.info('Vaccine Sentiment Database created successfully.')


def add_df(local_path):
    '''Adds clean dataframe to database either locally or in AWS RDS'''
    if os.environ.get('MYSQL_HOST') is None and\
       os.environ.get('SQLALCHEMY_DATABASE_URI') is None:
        logger.info('Database location: Local')
        logger.debug('Set MYSQL_HOST variable for AWS RDS instead of local')
    else:
        logger.info('Database location: AWS RDS')
        logger.debug('Remove MYSQL_HOST variable for local instead of AWS')
    # set up mysql connection
    engine = sql.create_engine(SQLALCHEMY_DATABASE_URI)

    df = pd.read_csv(local_path)
    try:
        df.to_sql('vaccine_response', engine, if_exists='replace', index=False)
        logger.info('Response data added to database')
    except sql.exc.OperationalError as e:
        logger.debug('Make sure you are connected to the VPN')
        logger.error("Error with sql functionality: ", e)
    except:
        logger.error("Uncaught error adding response data to database")


class ResponseManager:
    '''Class that aids in connecting to database for vaccine response'''

    def __init__(self, app=None, engine_string=None):
        '''Initialize class for RepsonseManager

        Args:
            self
            app (Flask app): initialized Flask application
            engine_string (str): engine string to connect to databases

        Returns:
            None
        '''
        if app:
            self.db = SQLAlchemy(app)
            self.session = self.db.session
        elif engine_string:
            engine = sql.create_engine(engine_string)
            Session = sessionmaker(bind=engine)
            self.session = Session()
        else:
            raise ValueError("Need either an engine string or a Flask app to initialize")
