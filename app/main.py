from fastapi import FastAPI, status

from app.api.category import router as category_router
from app.api.product import router as product_router


app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
async def welcome() -> dict:
    return {
        "message": "Добро пожаловать в API Проект",
        "docs": "/docs",
        "redoc": "/redoc"
    }

app.include_router(category_router)
app.include_router(product_router)
