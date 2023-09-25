from fastapi import FastAPI

from orderful.core.settings import settings
from orderful.routers.authentication import router as auth_router
from orderful.routers.orders import router as order_router
from orderful.routers.products import router as product_router

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.REST_ROUTE}/openapi.json")
app.include_router(auth_router, prefix=settings.REST_ROUTE, tags=["Authentication"])
app.include_router(product_router, prefix=settings.REST_ROUTE, tags=["Products"])
app.include_router(order_router, prefix=settings.REST_ROUTE, tags=["Orders"])
