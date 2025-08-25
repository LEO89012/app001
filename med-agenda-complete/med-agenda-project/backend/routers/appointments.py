from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from models import Cita, Profesional
from crud import get_session
from sqlmodel import select
from utils.mailer import send_mail
from utils.notify import send_whatsapp
import asyncio

from auth import get_current_user

router = APIRouter()

@router.get('/')
def list_citas(profesional_id: Optional[int] = None, estado: Optional[str] = None, mes: Optional[str] = None, cipac: Optional[str] = None):
    s = get_session()
    q = select(Cita, Profesional).join(Profesional, Cita.profesional_id == Profesional.id)
    if profesional_id:
        q = q.where(Cita.profesional_id == profesional_id)
    if estado:
        q = q.where(Cita.estado == estado)
    if mes:
        # mes in format YYYY-MM
        start = f"{mes}-01"
        end = f"{mes}-31"
        q = q.where(Cita.fecha >= start).where(Cita.fecha <= end)
    if cipac:
        q = q.where(Profesional.cipac == cipac)
    rows = s.exec(q).all()
    # flatten
    result = []
    for c, p in rows:
        item = c.dict()
        item['profesional'] = p.nombre
        item['cipac'] = p.cipac
        result.append(item)
    return result

@router.post('/')
def create_cita(cita: Cita):
    s = get_session()
    s.add(cita)
    s.commit()
    s.refresh(cita)
    # Notifications (async)
    async def notify():
        try:
            prof = s.exec(select(Profesional).where(Profesional.id==cita.profesional_id)).first()
            if prof and prof.correo:
                await send_mail(prof.correo, 'Nueva cita agendada', f'<p>Se ha agendado una nueva cita: {cita.fecha} {cita.hora_inicio}-{cita.hora_fin}</p>')
        except Exception as e:
            print('Notify error', e)
    try:
        asyncio.create_task(notify())
    except Exception:
        pass
    return {'id': cita.id}


from fastapi import HTTPException
from sqlmodel import select
from utils.mailer import send_mail
from utils.notify import send_whatsapp
import asyncio

from datetime import datetime

@router.patch('/{id}')
def update_cita(id: int, fecha: str = None, hora_inicio: str = None, hora_fin: str = None, estado: str = None):
    s = get_session()
    q = select(Cita).where(Cita.id == id)
    cita = s.exec(q).first()
    if not cita:
        raise HTTPException(status_code=404, detail='Cita no encontrada')
    if fecha: cita.fecha = fecha
    if hora_inicio: cita.hora_inicio = hora_inicio
    if hora_fin: cita.hora_fin = hora_fin
    if estado: cita.estado = estado
    s.add(cita); s.commit(); s.refresh(cita)
    return {'ok': True, 'id': cita.id}
