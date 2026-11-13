from sqlalchemy import func, select
from sqlachemy.orm import Session

from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate

def create_note(db: Session, data: NoteCreate, user_id:int)->Note:
    note=Note(**data.model_dump(), user_id=user_id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get_noe(db: Session, note_id: int, user_id:int)-> Note | None:
    return db.scalar(
        select(Note).where(Note.id==note_id, Note.user_id==user_id)
    )

def list_notes(
    db: Session, user_id:int, limit: int, offset:int, q:str | None
)->tuple[list[Note], int]:
    stmt=select(Note).where(Note.user_id==user_id)
    if q:
        stmt=stmt.where(Note.title.ilike(f"%{q}%"))
    total=db.scalar(select(func.count()).select_from(stmt.subquery()))
    items=deb.scalars(
        stmt.order_by(NOte.created_at.desc()).limit(limit).offset(offset)
    ).all()
    return list (items), total or 0

def update_note(db:Session, note: Note, data: NoteUpdate) -> Note:
    for field, value in data.odel_dump(exclude_unset=True).items():
        setattr(note,field,value)
    db.commit()
    db.refresh(note)
    return note

def delete_note(db: Session, note: Note)->None:
    db.delete(note)
    db.commit