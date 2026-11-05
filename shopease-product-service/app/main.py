from fastapi import FastAPI
from app.routers import product_routes

app = FastAPI(
    title="ShopEase Product Service",
    description="Microservice for managing e-commerce products",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "ShopEase Product Service is running",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "service": "product-service",
        "status": "healthy"
    }


app.include_router(product_routes.router)
