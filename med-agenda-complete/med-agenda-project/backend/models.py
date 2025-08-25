from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date, time

class Empresa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    nit: Optional[str] = None
    estado: str = 'Activa'
    creado_en: datetime = Field(default_factory=datetime.utcnow)

class Programa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None

class Municipio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    departamento: Optional[str] = None

class Poliza(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    numero_poliza: str
    aseguradora: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

class Profesional(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    especialidad: Optional[str] = None
    correo: str
    contrasena: str
    telefono: Optional[str] = None
    municipio_id: Optional[int] = Field(default=None, foreign_key='municipio.id')
    poliza_id: Optional[int] = Field(default=None, foreign_key='poliza.id')
    empresa_id: Optional[int] = Field(default=None, foreign_key='empresa.id')
    cipac: Optional[str] = None
    creado_en: datetime = Field(default_factory=datetime.utcnow)

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    correo: str
    contrasena: str
    nombre: str
    rol_id: Optional[int] = Field(default=None, foreign_key='role.id')
    profesional_id: Optional[int] = Field(default=None, foreign_key='profesional.id')
    empresa_id: Optional[int] = Field(default=None, foreign_key='empresa.id')
    creado_en: datetime = Field(default_factory=datetime.utcnow)

class Cita(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profesional_id: int = Field(foreign_key='profesional.id')
    fecha: date
    hora_inicio: str
    hora_fin: str
    estado: str = 'Agendada'
    descripcion: Optional[str] = None
    empresa_id: Optional[int] = Field(default=None, foreign_key='empresa.id')
    creado_en: datetime = Field(default_factory=datetime.utcnow)

class HoraTrabajada(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profesional_id: int = Field(foreign_key='profesional.id')
    fecha: date
    horas: float
    observacion: Optional[str] = None
    creado_en: datetime = Field(default_factory=datetime.utcnow)

class Documento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profesional_id: Optional[int] = Field(default=None, foreign_key='profesional.id')
    cita_id: Optional[int] = Field(default=None, foreign_key='cita.id')
    nombre_archivo: str
    ruta: str
    mime: Optional[str] = 'application/pdf'
    creado_en: datetime = Field(default_factory=datetime.utcnow)
