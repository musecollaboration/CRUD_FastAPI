from app.schemas.product import ProductShort
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing_extensions import Annotated
from typing import Literal


class CategoryShort(BaseModel):
    id: Annotated[int, Field(description="ID категории")]
    name: Annotated[str, Field(description="Название категории")]


class CategoryRead(BaseModel):
    id: Annotated[int, Field(description="ID категории")]
    name: Annotated[str, Field(description="Название категории")]
    slug: Annotated[str, Field(description="Уникальный slug")]
    is_active: Annotated[bool, Field(description="Категория активна")]
    parent_id: Annotated[int | None, Field(default=None, description="ID родительской категории")]
    products: Annotated[list[int], Field(description="Список продуктов в категории")]
    parent: Annotated[CategoryShort | None, Field(description="Родительская категория")]

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=100, description="Название категории")]
    parent_id: Annotated[int | None, Field(default=None, description="ID родительской категории")]

    model_config = ConfigDict(from_attributes=True)

    @field_validator('name')
    def name_must_not_contain_special_chars(cls, v):
        if any(char in v for char in ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']):
            raise ValueError('Имя категории не должно содержать специальные символы')
        return v


class CategoryUpdate(BaseModel):
    name: Annotated[str | None, Field(default=None, min_length=2, max_length=100, description="Название категории")]
    is_active: Annotated[bool | None, Field(default=None, description="Категория активна")]
    parent_id: Annotated[int | None, Field(default=None, description="ID родительской категории")]

    model_config = ConfigDict(from_attributes=True)


class FlatNode(BaseModel):
    id: Annotated[int, Field(description="ID категории или товара")]
    name: Annotated[str, Field(description="Название")]
    price: Annotated[float | None, Field(default=None, description="Цена товара")] = None
    type: Annotated[Literal["category", "product"], Field(description="Тип узла")]
    parentId: Annotated[int | None, Field(description="ID родителя (категории)")]

    model_config = dict(from_attributes=True)


class CategoryTreeWithProducts(CategoryShort):
    children: Annotated[list['CategoryTreeWithProducts'], Field(description="Вложенные категории")] = []
    products: Annotated[list[ProductShort], Field(description="Товары в категории")] = []


CategoryTreeWithProducts.model_rebuild()
