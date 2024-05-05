from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import logging

# TEST_MODE = config('TEST_MODE', default=False, cast=bool)

# DB_URL = config('DB_URL_TEST') if TEST_MODE else config('DB_URL')

# logging.basicConfig(filename='sqlalchemy.log', level=logging.INFO)

# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

DB_URL = config('DB_URL')

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine, autoflush=True)
