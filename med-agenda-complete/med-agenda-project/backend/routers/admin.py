from fastapi import APIRouter
from crud import get_session
from auth import require_role, get_current_user
from fastapi import Depends, HTTPException
from sqlmodel import select
from models import Empresa

from models import Empresa
from sqlmodel import select

router = APIRouter()

@router.get('/empresas')
def list_empresas():
    s = get_session()
    q = select(Empresa)
    return s.exec(q).all()


from fastapi.responses import StreamingResponse
import io, csv
from sqlmodel import func

@router.get('/kpis')
def kpis():
    s = get_session()
    total_emp = s.exec(select(Empresa)).count()
    total_prof = s.exec(select(Profesional)).count()
    total_citas = s.exec(select(Cita)).count()
    return {'empresas': total_emp, 'profesionales': total_prof, 'citas': total_citas}

@router.get('/export/citas/csv')
def export_citas_csv(desde: str = None, hasta: str = None):
    s = get_session()
    q = select(Cita, Profesional).join(Profesional, Cita.profesional_id == Profesional.id)
    if desde: q = q.where(Cita.fecha >= desde)
    if hasta: q = q.where(Cita.fecha <= hasta)
    rows = s.exec(q).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['id','fecha','hora_inicio','hora_fin','estado','profesional','empresa_id','descripcion'])
    for c,p in rows:
        writer.writerow([c.id, c.fecha, c.hora_inicio, c.hora_fin, c.estado, p.nombre, c.empresa_id, c.descripcion or ''])
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]), media_type='text/csv', headers={'Content-Disposition':'attachment; filename="citas.csv"'})


@router.post('/empresas')
def create_empresa(payload: dict, user = Depends(require_role(['admin']))):
    s = get_session()
    e = Empresa(nombre=payload.get('nombre'), nit=payload.get('nit'))
    s.add(e); s.commit(); s.refresh(e)
    return e

@router.delete('/empresas/{id}')
def delete_empresa(id: int, user = Depends(require_role(['admin']))):
    s = get_session()
    q = select(Empresa).where(Empresa.id == id)
    e = s.exec(q).first()
    if not e:
        raise HTTPException(status_code=404, detail='Empresa no encontrada')
    s.delete(e); s.commit()
    return {'ok': True}
