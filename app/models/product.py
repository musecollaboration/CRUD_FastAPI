from sqlalchemy import Float, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.backend.db import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)

    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False
    )
    category: Mapped['Category'] = relationship("Category", back_populates="products")  # type: ignore

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, in_stock={self.in_stock})>"
