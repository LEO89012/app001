from crud import init_db, get_session
from models import Empresa, Programa, Municipio, Poliza, Profesional, Role, Usuario, Cita, HoraTrabajada
from passlib.hash import bcrypt
from datetime import date

def seed():
    init_db()
    s = get_session()
    # empresas
    e1 = Empresa(nombre='Empresa Salud A', nit='900111222')
    e2 = Empresa(nombre='Empresa Salud B', nit='900222333')
    e3 = Empresa(nombre='Empresa Salud C', nit='900333444')
    s.add_all([e1,e2,e3]); s.commit()
    # programas, municipios, polizas
    p1 = Programa(nombre='Programa A', descripcion='Desc A'); p2 = Programa(nombre='Programa B')
    m1 = Municipio(nombre='Bogotá', departamento='Cundinamarca'); m2 = Municipio(nombre='Medellín', departamento='Antioquia')
    pol1 = Poliza(numero_poliza='POL-0001', aseguradora='Aseguradora Uno')
    s.add_all([p1,p2,m1,m2,pol1]); s.commit()
    # roles
    r_admin = Role(nombre='admin'); r_prof = Role(nombre='profesional'); s.add_all([r_admin, r_prof]); s.commit()
    # profesionales
    prof1 = Profesional(nombre='Dr. Juan Pérez', especialidad='Medicina General', correo='juan.perez@empresa.com', contrasena=bcrypt.hash('pass123'), telefono='3001112222', municipio_id=m1.id, poliza_id=pol1.id, empresa_id=e1.id, cipac='CIPAC001')
    prof2 = Profesional(nombre='Dra. Laura Gómez', especialidad='Odontología', correo='laura.gomez@empresa.com', contrasena=bcrypt.hash('pass123'), telefono='3002223333', municipio_id=m2.id, poliza_id=pol1.id, empresa_id=e2.id, cipac='CIPAC002')
    s.add_all([prof1, prof2]); s.commit()
    # usuarios
    uadmin = Usuario(correo='admin@medagenda.com', contrasena=bcrypt.hash('adminpass'), nombre='Admin Global', rol_id=r_admin.id)
    uprof = Usuario(correo='juan.perez@empresa.com', contrasena=prof1.contrasena, nombre=prof1.nombre, rol_id=r_prof.id, profesional_id=prof1.id, empresa_id=e1.id)
    s.add_all([uadmin, uprof]); s.commit()
    # citas
    c1 = Cita(profesional_id=prof1.id, fecha=date(2025,8,15), hora_inicio='08:00', hora_fin='08:30', estado='Agendada', descripcion='Consulta general', empresa_id=e1.id)
    c2 = Cita(profesional_id=prof2.id, fecha=date(2025,8,16), hora_inicio='09:00', hora_fin='09:30', estado='Realizada', descripcion='Limpieza dental', empresa_id=e2.id)
    s.add_all([c1,c2]); s.commit()
    print('Seed done.')

if __name__ == '__main__':
    seed()
