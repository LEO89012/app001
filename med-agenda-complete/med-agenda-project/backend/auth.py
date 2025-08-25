from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlmodel import select
from crud import get_session
from models import Usuario
from passlib.hash import bcrypt
import os
from datetime import datetime, timedelta

SECRET = os.environ.get('JWT_SECRET', 'supersecretkey')
ALGORITHM = 'HS256'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/token')

def authenticate_user(email: str, password: str):
    s = get_session()
    q = select(Usuario).where(Usuario.correo == email)
    user = s.exec(q).first()
    if not user: return None
    if not bcrypt.verify(password, user.contrasena): return None
    return user

def create_access_token(data: dict, expires_minutes: int = 480):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    s = get_session()
    q = select(Usuario).where(Usuario.correo == email)
    user = s.exec(q).first()
    if user is None:
        raise credentials_exception
    return user


from fastapi import Depends, HTTPException, status

def require_role(roles: list):
    def role_checker(user = Depends(get_current_user)):
        # user is Usuario model instance
        if not hasattr(user, 'rol_id'):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No role info')
        # map rol_id to name via DB
        s = get_session()
        from models import Role
        r = s.exec(select(Role).where(Role.id == user.rol_id)).first()
        rol_name = r.nombre if r else None
        if rol_name not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Insufficient permissions')
        return user
    return role_checker
