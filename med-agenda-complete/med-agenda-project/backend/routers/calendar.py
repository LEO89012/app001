from fastapi import APIRouter
from crud import get_session
from models import Cita, Profesional
from sqlmodel import select

router = APIRouter()

@router.get('/events')
def events():
    s = get_session()
    q = select(Cita, Profesional).join(Profesional, Cita.profesional_id == Profesional.id)
    rows = s.exec(q).all()
    events = []
    for c,p in rows:
        events.append({
            'id': c.id,
            'title': f"{p.nombre} ({c.estado})",
            'start': f"{c.fecha}T{c.hora_inicio}",
            'end': f"{c.fecha}T{c.hora_fin}"
        })
    return events
