from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path
from db.model import Base

PATH = os.path.dirname(os.path.realpath(__file__))
engine = create_engine('sqlite:///' + PATH + '/../tagdb.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
dbsession = DBSession()