from fastapi import FastAPI
from app.db.connection import sessionmaker
app = FastAPI()

Session = sessionmaker()


@app.get('/test')
def route_test():
    return {'message': 'OK'}
