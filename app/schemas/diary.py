from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class DiaryEntryBase(BaseModel):
    """Схема для записи в ежедневнике"""
    title: str = Field(..., min_length=1, max_length=200, description="Заголовок записи")
    content: str = Field(..., min_length=1, description="Содержание записи")


class DiaryEntryCreate(DiaryEntryBase):
    """Схема для создания новой записи"""
    pass


class DiaryEntryUpdate(BaseModel):
    """Схема для обновления записи (все поля опциональны)"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)


class DiaryEntryResponse(DiaryEntryBase):
    """Схема ответа с полной информацией о записи"""
    id: int
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class DiaryEntryCompleteToggle(BaseModel):
    """Схема для изменения статуса выполнения"""
    is_completed: bool = Field(..., description="Статус выполнения записи")


class MessageResponse(BaseModel):
    """Схема ответа с текстовым сообщением"""
    message: str