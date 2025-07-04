from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app.backend.dependencies import get_db
from app.crud import product as crud
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductRead])
def get_all_products(db: Annotated[Session, Depends(get_db)]):
    return crud.get_all_products(db)


@router.post("/", response_model=ProductRead)
def create_product(
    product_data: ProductCreate,
    db: Annotated[Session, Depends(get_db)]
):
    return crud.create_product(db, product_data)


@router.patch("/{product_id}", response_model=ProductRead, status_code=status.HTTP_200_OK)
def patch_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Annotated[Session, Depends(get_db)]
):
    if product_data.model_dump(exclude_unset=True) == {}:
        raise HTTPException(status_code=400, detail="Нет данных для обновления")

    product = crud.update_product(db, product_id, product_data)
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return product


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Annotated[Session, Depends(get_db)]):
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return product


@router.delete("/{product_id}", status_code=200)
def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db)
) -> JSONResponse:
    crud.delete_product(db, product_id)
    return JSONResponse(content={"detail": "Продукт удалён"}, status_code=200)
