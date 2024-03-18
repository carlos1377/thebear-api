from fastapi import FastAPI
from app.routes.category import router as category_router

app = FastAPI()


@app.get('/test')
def route_test():
    return {'message': 'OK'}


app.include_router(category_router)
