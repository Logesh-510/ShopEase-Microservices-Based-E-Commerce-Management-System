from fastapi import FastAPI

from app.routers import user_routes, address_routes

app = FastAPI(
    title="ShopEase User Management Service",
    description=(
        "User profile and address management "
        "microservice for ShopEase"
    ),
    version="1.0.0"
)


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "ShopEase User Management Service is running",
        "status": "success"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "service": "User Service",
        "status": "healthy"
    }


app.include_router(user_routes.router)
app.include_router(address_routes.router)
