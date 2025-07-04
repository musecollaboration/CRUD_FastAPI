from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app.backend.dependencies import get_db
from app.crud import category as crud
from app.schemas.category import CategoryCreate, CategoryRead, CategoryTreeWithProducts, CategoryUpdate, FlatNode


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get("/", response_model=list[CategoryRead], status_code=status.HTTP_200_OK)
def get_all_categories(
    db: Annotated[Session, Depends(get_db)]
):
    return crud.get_all_categories(db)


@router.get("/flat-tree", response_model=list[FlatNode])
def get_flat_tree(
    db: Annotated[Session, Depends(get_db)]
):
    return crud.get_flat_tree(db)


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    db: Annotated[Session, Depends(get_db)]
):
    return crud.create_category(db, category_data)


@router.get("/{category_id}", response_model=CategoryRead, status_code=status.HTTP_200_OK)
def get_category(
    category_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    category = crud.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category


@router.patch("/{category_id}", response_model=CategoryRead, status_code=status.HTTP_200_OK)
def patch_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Annotated[Session, Depends(get_db)]
):
    category = crud.update_category(db, category_id, category_data)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category


@router.delete("/{category_id}", status_code=200)
def delete_category_endpoint(
    category_id: int,
    db: Session = Depends(get_db)
) -> JSONResponse:
    crud.delete_category(db, category_id)
    return JSONResponse(content={"detail": "Категория удалена"}, status_code=200)


@router.get("/{category_id}/tree-with-products", response_model=CategoryTreeWithProducts)
def get_category_product_tree(
    category_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    tree = crud.get_category_product_tree_by_id(db, category_id)
    if not tree:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return tree
