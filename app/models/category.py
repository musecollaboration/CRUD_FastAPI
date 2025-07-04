from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.backend.db import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    parent_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=True
    )
    parent: Mapped['Category'] = relationship(
        "Category",
        remote_side=[id],
        back_populates='children',
    )
    products: Mapped[list['Product']] = relationship(  # type: ignore
        back_populates='category',
        cascade="all, delete-orphan"
    )
    children: Mapped[list['Category']] = relationship(
        "Category",
        back_populates="parent",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}', slug='{self.slug}')>"
