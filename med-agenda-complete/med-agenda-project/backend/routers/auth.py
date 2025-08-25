from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth import authenticate_user, create_access_token
from models import Usuario
from sqlmodel import select
from crud import get_session

router = APIRouter()

@router.post('/token')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        return {'error':'Invalid credentials'}
    token = create_access_token({'sub': user.correo})
    return {'access_token': token, 'token_type':'bearer'}
