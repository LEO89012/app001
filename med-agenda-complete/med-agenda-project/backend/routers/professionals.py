from fastapi import APIRouter, Depends
from typing import List
from auth import get_current_user
from crud import get_session
from models import Profesional
from sqlmodel import select

router = APIRouter()

@router.get('/', response_model=List[Profesional])
def list_professionals():
    s = get_session()
    q = select(Profesional)
    rows = s.exec(q).all()
    return rows
