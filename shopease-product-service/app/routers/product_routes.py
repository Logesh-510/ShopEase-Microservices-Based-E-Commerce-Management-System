from fastapi import APIRouter, HTTPException, Query, status

from app.config.settings import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.schemas.product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse
)
from app.services import product_service


router = APIRouter(
    prefix="/api/products",
    tags=["Products"]
)


@router.get("/health")
def product_router_health():
    return {
        "message": "Product Router is working",
        "status": "success"
    }


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate):
    return product_service.create_product(product_data.model_dump())


@router.get("/", response_model=list[ProductResponse])
def get_all_products(
    category: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(DEFAULT_PAGE_SIZE, gt=0, le=MAX_PAGE_SIZE)
):
    return product_service.get_all_products(
        category=category,
        skip=skip,
        limit=limit
    )


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int):
    product = product_service.get_product_by_id(product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_data: ProductUpdate):
    update_data = product_data.model_dump(
        exclude_unset=True,
        exclude_none=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="At least one field must be provided"
        )

    product = product_service.update_product(product_id, update_data)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    product = product_service.delete_product(product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return None
