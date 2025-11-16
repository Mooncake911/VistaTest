from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_tables, drop_tables
from app.routers import entries_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # drop_tables()
    create_tables()
    print("✅ Application started - tables created")
    yield
    print("🛑 Application shutting down")


app = FastAPI(
    title="Diary Backend API",
    description="API для управления ежедневником с возможностью создания, чтения, обновления и удаления записей",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS (для фронтенда)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(entries_router)


@app.get("/", tags=["Root"])
async def root():
    """
    Корневой эндпоинт API.
    Возвращает информацию о приложении.
    """
    return {
        "message": "Добро пожаловать в Diary Backend API!",
        "version": "1.0.0",
        "developer": "Mooncake911 (Shaidurov Vadim)",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Проверка работоспособности API.
    """
    return {"status": "healthy", "service": "diary-api"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
