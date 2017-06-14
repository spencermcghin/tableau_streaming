# Imports
from sqlalchemy import create_engine, MetaData, Column, String, Integer, Table

# Local Imports
from settings import SQLALCHEMY_DATABASE_URI

# Instantiate db objects
engine = create_engine(SQLALCHEMY_DATABASE_URI)
conn = engine.raw_connection()
meta = MetaData(bind=engine)


# Create table for mysql dataframe storage

table_hack_attacks = Table('hack_attacks', meta,
    Column('id', Integer, primary_key=True),
    Column('index', Integer),
    Column('attack_type', String(50)),
    Column('attacker_ip', String(50)),
    Column('attack_port', String(50)),
    Column('latitude2', String(50)),
    Column('longitude2', String(50)),
    Column('longitude', String(50)),
    Column('city_target', String(50)),
    Column('country_target', String(10)),
    Column('attack_subtype', String(50)),
    Column('latitude', String(50)),
    Column('city_origin', String(50)),
    Column('country_origin', String(2)))


# Create table via sqlalchemy
meta.create_all(engine)
