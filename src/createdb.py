import logging.config
import os

import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer
from config.flaskconfig import SQLALCHEMY_DATABASE_URI

logger = logging.getLogger(__name__)

Base = declarative_base()


class VaccineSentiment(Base):
    '''Create a table used to store clean data for application use'''
    __tablename__ = 'vaccine_clean'
    id = Column(Integer, primary_key=True)
    EGENDER = Column(Integer, unique=False, nullable=True)
    RRACE = Column(Integer, unique=False, nullable=True)
    EEDUC = Column(Integer, unique=False, nullable=True)
    MS = Column(Integer, unique=False, nullable=True)
    KINDWORK = Column(Integer, unique=False, nullable=True)
    REGION = Column(Integer, unique=False, nullable=True)
    TBIRTH_YEAR = Column(Integer, unique=False, nullable=True)
    WHYNOT1 = Column(Integer, unique=False, nullable=True)
    WHYNOT2 = Column(Integer, unique=False, nullable=True)
    WHYNOT3 = Column(Integer, unique=False, nullable=True)
    WHYNOT4 = Column(Integer, unique=False, nullable=True)
    WHYNOT5 = Column(Integer, unique=False, nullable=True)
    WHYNOT6 = Column(Integer, unique=False, nullable=True)
    WHYNOT7 = Column(Integer, unique=False, nullable=True)
    WHYNOT8 = Column(Integer, unique=False, nullable=True)
    WHYNOT9 = Column(Integer, unique=False, nullable=True)
    WHYNOT10 = Column(Integer, unique=False, nullable=True)
    WHYNOT11 = Column(Integer, unique=False, nullable=True)

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

    if os.environ.get('MYSQL_HOST') is None:
        logger.info('Database location: Local')
        logger.debug('Set MYSQL_HOST variable for AWS RDS instead of local')
    else:
        logger.info('Database location: AWS RDS')
        logger.debug('Remove MYSQL_HOST variable for local instead of AWS')
    # set up mysql connection
    engine = sql.create_engine(SQLALCHEMY_DATABASE_URI)

    df.to_sql('vaccine_clean', engine, if_exists='replace', index=False)
    # try:
    #
    # except:
    #     logger.error("Error adding clean data to database")
