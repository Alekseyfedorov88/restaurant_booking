from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.table import Table
from app.database import get_session
from typing import List

router = APIRouter(prefix="/tables", tags=["Tables"])

@router.get("/", response_model=List[Table])
def get_tables(session: Session = Depends(get_session)):
    tables = session.exec(select(Table)).all()
    return tables

@router.post("/", response_model=Table)
def create_table(table: Table, session: Session = Depends(get_session)):
    session.add(table)
    session.commit()
    session.refresh(table)
    return table

@router.delete("/{table_id}")
def delete_table(table_id: int, session: Session = Depends(get_session)):
    table = session.get(Table, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    session.delete(table)
    session.commit()
    return {"ok": True}
