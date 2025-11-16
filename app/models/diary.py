from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base


class DiaryEntry(Base):
    """
    Модель записи в ежедневнике.

    Attributes:
        id: Уникальный идентификатор записи
        title: Заголовок записи
        content: Содержимое записи
        is_completed: Флаг выполнения задачи
        created_at: Дата и время создания
        updated_at: Дата и время последнего обновления
    """
    __tablename__ = "diary_entries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<DiaryEntry(id={self.id}, title='{self.title}', completed={self.is_completed})>"