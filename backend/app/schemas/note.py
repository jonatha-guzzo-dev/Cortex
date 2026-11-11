from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class NoteBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    url: str | None=Field(default=None, max_length=2048)

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1,max_length= 200)
    content: str | None = Field(default=None, min_length=1)
    url: str | None = Field(default=None, max_length=2048)

class NoteRead(NoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    summary: str | None
    created_at: datetime
    updated_at: datetime


class NoteList(BaseModel):
    items: list[NoteRead]
    total: int
    limit: int
    offset: int
