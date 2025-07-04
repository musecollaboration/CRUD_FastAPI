from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing_extensions import Annotated


class ProductCreate(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=100, description="Имя продукта")]
    price: Annotated[float, Field(description="Цена продукта")]
    category_id: Annotated[int, Field(description="ID категории")]

    model_config = ConfigDict(from_attributes=True)

    @field_validator('name')
    def name_must_not_contain_special_chars(cls, v):
        if any(char in v for char in ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']):
            raise ValueError('Имя продукта не должно содержать специальные символы')
        return v


class ProductUpdate(BaseModel):
    name: Annotated[str | None, Field(default=None, min_length=2, max_length=100, description="Имя продукта")]
    price: Annotated[float | None, Field(default=None, description="Цена продукта")]
    category_id: Annotated[int | None, Field(default=None, description="ID категории")]

    model_config = ConfigDict(from_attributes=True)

    @field_validator('name')
    def name_must_not_contain_special_chars(cls, v):
        if any(char in v for char in ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']):
            raise ValueError('Имя продукта не должно содержать специальные символы')
        return v


class ProductRead(BaseModel):
    id: Annotated[int, Field]
    name: Annotated[str, Field(min_length=2, max_length=100, description="Имя должно содержать от 2 до 100 символов")]
    price: Annotated[float, Field(description="Цена продукта")]
    category_id: Annotated[int | None, Field(description='ID категории')]
    category_name: Annotated[str | None, Field(description="Название категории")] = None

    model_config = ConfigDict(from_attributes=True)


class ProductShort(BaseModel):
    id: Annotated[int, Field(description="ID товара")]
    name: Annotated[str, Field(description="Название товара")]
    price: Annotated[float, Field(description="Цена товара")]
