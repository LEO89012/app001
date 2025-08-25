from sqlmodel import Session, select
from models import *
from sqlmodel import SQLModel, create_engine
from typing import List, Optional
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///./med_agenda.db')
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
