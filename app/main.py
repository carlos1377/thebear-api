from fastapi import FastAPI
from app.routes.category import router as category_router
from app.routes.product import router as product_router
from app.routes.client import router as client_router
from app.routes.user import router as user_router


app = FastAPI()


@app.get('/health-check')
def route_test():
    return {'message': 'OK'}


app.include_router(category_router)
app.include_router(product_router)
app.include_router(client_router)
app.include_router(user_router)
