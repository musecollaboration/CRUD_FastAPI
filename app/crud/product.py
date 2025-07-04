from fastapi import HTTPException
from app.models import Product
from sqlalchemy.orm import Session
from sqlalchemy import select
from slugify import slugify
from app.models.product import Product as ProductModel
from app.schemas.product import ProductUpdate, ProductRead, ProductCreate
from sqlalchemy.orm import joinedload


def get_all_products(db: Session) -> list[ProductRead]:
    stmt = (
        select(ProductModel)
        .options(joinedload(ProductModel.category))
        .where(ProductModel.is_active.is_(True))
    )
    products = db.scalars(stmt).all()

    return [
        ProductRead(
            id=product.id,
            name=product.name,
            price=product.price,
            category_id=product.category_id,
            category_name=product.category.name if product.category else None
        )
        for product in products
    ]


def create_product(db: Session, product_data: ProductCreate) -> ProductRead:
    product = ProductModel(
        name=product_data.name,
        slug=slugify(product_data.name),
        price=product_data.price,
        category_id=product_data.category_id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return ProductRead(
        id=product.id,
        name=product.name,
        price=product.price,
        category_id=product.category_id,
        category_name=product.category.name if product.category else None
    )


def update_product(db: Session, product_id: int, data: ProductUpdate) -> ProductRead | None:
    product = db.get(ProductModel, product_id)
    if not product:
        return None

    updates = data.model_dump(exclude_unset=True)

    if "name" in updates:
        product.name = updates["name"]
        product.slug = slugify(product.name)

    if "price" in updates:
        product.price = updates["price"]

    if "category_id" in updates:
        product.category_id = updates["category_id"]

    db.commit()
    db.refresh(product)
    return ProductRead(
        id=product.id,
        name=product.name,
        price=product.price,
        category_id=product.category_id,
        category_name=product.category.name if product.category else None
    )


def get_product_by_id(db: Session, product_id: int) -> ProductRead | None:
    product = db.get(ProductModel, product_id)
    return ProductRead(
        id=product.id,
        name=product.name,
        price=product.price,
        category_id=product.category_id,
        category_name=product.category.name
    )


def delete_product(db: Session, product_id: int) -> None:
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    db.delete(product)
    db.commit()
