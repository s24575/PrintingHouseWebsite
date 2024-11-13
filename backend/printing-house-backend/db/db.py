import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.getenv("PRINTING_HOUSE_DATABASE_URI"))

Session = sessionmaker(bind=engine)

db = None
