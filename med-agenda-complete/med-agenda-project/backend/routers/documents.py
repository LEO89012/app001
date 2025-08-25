from fastapi import APIRouter, UploadFile, File, Form, Depends
import os, shutil
from crud import get_session
from models import Documento
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post('/upload')
def upload(file: UploadFile = File(...), cita_id: int = Form(...), profesional_id: int = Form(None)):
    filename = f"{int(datetime.utcnow().timestamp())}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, 'wb') as f:
        shutil.copyfileobj(file.file, f)
    s = get_session()
    doc = Documento(profesional_id=profesional_id, cita_id=cita_id, nombre_archivo=file.filename, ruta=path, mime=file.content_type)
    s.add(doc); s.commit(); s.refresh(doc)
    return {'id': doc.id, 'path': doc.ruta}

@router.get('/appointment/{id}')
def list_docs(id: int):
    s = get_session()
    q = select(Documento).where(Documento.cita_id == id)
    rows = s.exec(q).all()
    return rows
