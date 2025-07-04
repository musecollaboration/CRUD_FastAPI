from fastapi import HTTPException, status
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.category import Category as CategoryModel
from app.schemas.category import (CategoryCreate, CategoryRead, CategoryShort, CategoryTreeWithProducts, CategoryUpdate,
                                  FlatNode)
from app.schemas.product import ProductShort


def get_all_categories(db: Session) -> list[CategoryRead]:
    stmt = select(CategoryModel).where(CategoryModel.is_active.is_(True))
    categories = db.scalars(stmt).unique().all()

    return [
        CategoryRead(
            id=cat.id,
            name=cat.name,
            slug=cat.slug,
            is_active=cat.is_active,
            parent_id=cat.parent_id,
            parent=CategoryShort(
                id=cat.parent.id,
                name=cat.parent.name
            ) if cat.parent else None,
            products=[p.id for p in cat.products],
        )
        for cat in categories
    ]


def get_category_by_id(db: Session, category_id: int) -> CategoryRead | None:
    stmt = (
        select(CategoryModel)
        .options(joinedload(CategoryModel.products), joinedload(CategoryModel.parent))
        .where(CategoryModel.id == category_id)
    )
    cat = db.scalars(stmt).first()
    if not cat:
        return None

    return CategoryRead(
        id=cat.id,
        name=cat.name,
        slug=cat.slug,
        is_active=cat.is_active,
        parent_id=cat.parent_id,
        parent=CategoryShort(
            id=cat.parent.id,
            name=cat.parent.name
        ) if cat.parent else None,
        products=[p.id for p in cat.products],
    )


def create_category(db: Session, data: CategoryCreate) -> CategoryRead:
    category = CategoryModel(
        name=data.name,
        slug=slugify(data.name),
        is_active=True,
        parent_id=data.parent_id
    )
    db.add(category)
    db.commit()
    db.refresh(category)

    return CategoryRead(
        id=category.id,
        name=category.name,
        slug=category.slug,
        is_active=category.is_active,
        parent_id=category.parent_id,
        products=[],
        parent=None
    )


def update_category(db: Session, category_id: int, data: CategoryUpdate) -> CategoryRead | None:
    category = db.get(CategoryModel, category_id)
    if not category:
        return None

    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)

    return CategoryRead(
        id=category.id,
        name=category.name,
        slug=category.slug,
        is_active=category.is_active,
        parent_id=category.parent_id,
        parent=CategoryShort(
            id=category.parent.id,
            name=category.parent.name
        ) if category.parent else None,
        products=[p.id for p in category.products],
    )


def delete_category(db: Session, category_id: int) -> None:
    category = db.get(CategoryModel, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")

    db.delete(category)
    db.commit()


def build_category_product_tree(category: CategoryModel) -> CategoryTreeWithProducts:
    return CategoryTreeWithProducts(
        id=category.id,
        name=category.name,
        products=[
            ProductShort(id=p.id, name=p.name, price=p.price)
            for p in category.products if p.is_active
        ],
        children=[
            build_category_product_tree(child)
            for child in category.children if child.is_active
        ]
    )


def get_category_product_tree_by_id(db: Session, category_id: int) -> CategoryTreeWithProducts | None:
    stmt = (
        select(CategoryModel)
        .where(CategoryModel.id == category_id)
        .options(
            joinedload(CategoryModel.children).joinedload(CategoryModel.products),
            joinedload(CategoryModel.products)
        )
    )
    category = db.scalars(stmt).first()
    if not category:
        return None

    return build_category_product_tree(category)


def get_flat_tree(db: Session) -> list[FlatNode]:
    stmt = (
        select(CategoryModel)
        .options(joinedload(CategoryModel.products))
    )
    categories = db.scalars(stmt).unique().all()

    flat: list[FlatNode] = []

    for cat in categories:
        flat.append(FlatNode(
            id=cat.id,
            name=cat.name,
            type="category",
            parentId=cat.parent_id
        ))

        for product in cat.products:
            flat.append(FlatNode(
                id=product.id,
                name=product.name,
                price=product.price,
                type="product",
                parentId=cat.id
            ))

    return flat
