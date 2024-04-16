from fastapi import FastAPI
from app.routes.category import router as category_router
from app.routes.product import router as product_router
from app.routes.client import router as client_router

app = FastAPI()


@app.get('/test')
def route_test():
    return {'message': 'OK'}


app.include_router(category_router)
app.include_router(product_router)
app.include_router(client_router)
