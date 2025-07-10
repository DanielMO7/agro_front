from fastapi import APIRouter
from app.api.v1.endpoints import user, auth, inventory, input, warehouse

api_v1_router = APIRouter()

# Rutas
api_v1_router.include_router(auth.router, tags=["Auth"])
api_v1_router.include_router(user.router, tags=["Users"])
api_v1_router.include_router(inventory.router, tags=["Inventories"])
api_v1_router.include_router(input.router, tags=["Inputs"])
api_v1_router.include_router(warehouse.router, tags=["Warehouses"])

