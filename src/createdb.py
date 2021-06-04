import logging.config
import os

import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from config.flaskconfig import SQLALCHEMY_DATABASE_URI

logger = logging.getLogger(__name__)

Base = declarative_base()


class VaccineSentiment(Base):
    '''Create a table used to store clean data for application use'''
    __tablename__ = 'vaccine_source'
    id = Column(Integer, primary_key=True)
    response = Column(Integer, unique=False, nullable=True)
    url = Column(String(200), unique=False, nullable=True)

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
        logger.info("Database created from %s",  SQLALCHEMY_DATABASE_URI)
    except sql.exc.OperationalError:
        logger.error('Unable to create database')
        logger.warning('Please connect to Northwestern VPN or campus WiFi,\
                        or remove MY_SQL env variable for local location')
    else:
        logger.info('Vaccine Sentiment Database created successfully.')


def add_df(df):
    '''Adds clean dataframe to database either locally or in AWS RDS'''
    if os.environ.get('MYSQL_HOST') is None:
        logger.info('Database location: Local')
        logger.debug('Set MYSQL_HOST variable for AWS RDS instead of local')
    else:
        logger.info('Database location: AWS RDS')
        logger.debug('Remove MYSQL_HOST variable for local instead of AWS')
    # set up mysql connection
    engine = sql.create_engine(SQLALCHEMY_DATABASE_URI)

    try:
        df.to_sql('vaccine_clean', engine, if_exists='replace', index=False)
        logger.info('Clean data added to database')
    except sql.exc.OperationalError as e:
        logger.debug('Make sure you are connected to the VPN')
        logger.error("Error with sql functionality: ", e)
    except:
        logger.error("Uncaught error adding clean data to database")
