from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app.models import DiaryEntry
from app.schemas import DiaryEntryCreate, DiaryEntryUpdate


def create_entry(db: Session, entry: DiaryEntryCreate) -> DiaryEntry:
    """
    Создать новую запись в ежедневнике.

    Args:
        db: Сессия базы данных
        entry: Данные для создания записи

    Returns:
        Созданная запись
    """
    db_entry = DiaryEntry(
        title=entry.title,
        content=entry.content
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def get_entry(db: Session, entry_id: int) -> Optional[DiaryEntry]:
    """
    Получить запись по ID.

    Args:
        db: Сессия базы данных
        entry_id: ID записи

    Returns:
        Запись или None, если не найдена
    """
    return db.query(DiaryEntry).filter(DiaryEntry.id == entry_id).first()


def get_entries(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        completed: Optional[bool] = None
) -> List[DiaryEntry]:
    """
    Получить список записей с пагинацией и фильтрацией.

    Args:
        db: Сессия базы данных
        skip: Количество записей для пропуска
        limit: Максимальное количество записей
        completed: Фильтр по статусу выполнения (None = все записи)

    Returns:
        Список записей
    """
    query = db.query(DiaryEntry)

    if completed is not None:
        query = query.filter(DiaryEntry.is_completed == completed)

    return query.order_by(desc(DiaryEntry.created_at)).offset(skip).limit(limit).all()


def update_entry(db: Session, entry_id: int, entry_update: DiaryEntryUpdate) -> Optional[DiaryEntry]:
    """
    Обновить запись.

    Args:
        db: Сессия базы данных
        entry_id: ID записи
        entry_update: Данные для обновления

    Returns:
        Обновлённая запись или None, если не найдена
    """
    db_entry = get_entry(db, entry_id)
    if not db_entry:
        return None

    update_data = entry_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_entry, field, value)

    db.commit()
    db.refresh(db_entry)
    return db_entry


def delete_entry(db: Session, entry_id: int) -> bool:
    """
    Удалить запись.

    Args:
        db: Сессия базы данных
        entry_id: ID записи

    Returns:
        True, если запись удалена, False, если не найдена
    """
    db_entry = get_entry(db, entry_id)
    if not db_entry:
        return False

    db.delete(db_entry)
    db.commit()
    return True


def toggle_entry_completion(db: Session, entry_id: int, is_completed: bool) -> Optional[DiaryEntry]:
    """
    Изменить статус выполнения записи.

    Args:
        db: Сессия базы данных
        entry_id: ID записи
        is_completed: Новый статус выполнения

    Returns:
        Обновлённая запись или None, если не найдена
    """
    db_entry = get_entry(db, entry_id)
    if not db_entry:
        return None

    db_entry.is_completed = is_completed
    db.commit()
    db.refresh(db_entry)
    return db_entry