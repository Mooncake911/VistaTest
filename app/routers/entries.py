from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import (
    DiaryEntryCreate,
    DiaryEntryUpdate,
    DiaryEntryResponse,
    DiaryEntryCompleteToggle,
    MessageResponse
)
from app.crud import (
    create_entry,
    get_entry,
    get_entries,
    update_entry,
    delete_entry,
    toggle_entry_completion
)

router = APIRouter(
    prefix="/entries",
    tags=["Записи в ежедневнике"]
)


@router.post("/", response_model=DiaryEntryResponse, status_code=status.HTTP_201_CREATED)
async def create_diary_entry(
        entry: DiaryEntryCreate,
        db: Session = Depends(get_db)
):
    """
    Создать новую запись в ежедневнике.

    - **title**: Заголовок записи (обязательно)
    - **content**: Содержание записи (обязательно)
    """
    return create_entry(db=db, entry=entry)


@router.get("/", response_model=List[DiaryEntryResponse])
async def read_diary_entries(
        skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
        limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей"),
        completed: Optional[bool] = Query(None, description="Фильтр по статусу выполнения"),
        db: Session = Depends(get_db)
):
    """
    Получить список всех записей с пагинацией и фильтрацией.

    - **skip**: Количество записей для пропуска (по умолчанию: 0)
    - **limit**: Максимальное количество записей (по умолчанию: 100)
    - **completed**: Фильтр по статусу (True/False/None для всех)
    """
    entries = get_entries(db=db, skip=skip, limit=limit, completed=completed)
    return entries


@router.get("/{entry_id}", response_model=DiaryEntryResponse)
async def read_diary_entry(
        entry_id: int,
        db: Session = Depends(get_db)
):
    """
    Получить конкретную запись по ID.

    - **entry_id**: ID записи
    """
    db_entry = get_entry(db=db, entry_id=entry_id)
    if db_entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись с ID {entry_id} не найдена"
        )
    return db_entry


@router.put("/{entry_id}", response_model=DiaryEntryResponse)
async def update_diary_entry(
        entry_id: int,
        entry: DiaryEntryUpdate,
        db: Session = Depends(get_db)
):
    """
    Обновить запись.

    - **entry_id**: ID записи
    - **title**: Новый заголовок (опционально)
    - **content**: Новое содержание (опционально)
    """
    db_entry = update_entry(db=db, entry_id=entry_id, entry_update=entry)
    if db_entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись с ID {entry_id} не найдена"
        )
    return db_entry


@router.delete("/{entry_id}", response_model=MessageResponse)
async def delete_diary_entry(
        entry_id: int,
        db: Session = Depends(get_db)
):
    """
    Удалить запись.

    - **entry_id**: ID записи для удаления
    """
    success = delete_entry(db=db, entry_id=entry_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись с ID {entry_id} не найдена"
        )
    return {"message": f"Запись с ID {entry_id} успешно удалена"}


@router.patch("/{entry_id}/complete", response_model=DiaryEntryResponse)
async def toggle_diary_entry_completion(
        entry_id: int,
        completion: DiaryEntryCompleteToggle,
        db: Session = Depends(get_db)
):
    """
    Изменить статус выполнения записи.

    - **entry_id**: ID записи
    - **is_completed**: Новый статус выполнения (true/false)
    """
    db_entry = toggle_entry_completion(
        db=db,
        entry_id=entry_id,
        is_completed=completion.is_completed
    )
    if db_entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись с ID {entry_id} не найдена"
        )
    return db_entry