from fastapi import FastAPI
from app.routes.category import router as category_router
from app.routes.product import router as product_router
from app.routes.client import router as client_router
from app.routes.order import router as order_router
from app.routes.check import router as check_router
from app.routes.user import router as user_router

app = FastAPI(version=1, title="The Bear API")


@app.get('/health-check', tags=['Health Check'])
def route_test():
    return {'message': 'OK'}


app.include_router(category_router)
app.include_router(product_router)
app.include_router(client_router)
app.include_router(order_router)
app.include_router(check_router)
app.include_router(user_router)
