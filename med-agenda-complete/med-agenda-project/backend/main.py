from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, appointments, professionals, documents, admin, calendar
import os
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import Request


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Return structured validation errors
    return JSONResponse(status_code=422, content={"detail": exc.errors(), "body": exc.body})


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # Log exception here in production (Sentry/Logs)
    return JSONResponse(status_code=500, content={"detail": str(exc)})


app = FastAPI(title='MedAgenda API (SQLite)')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth.router, prefix='/api/auth')
app.include_router(appointments.router, prefix='/api/appointments')
app.include_router(professionals.router, prefix='/api/professionals')
app.include_router(documents.router, prefix='/api/documents')
app.include_router(admin.router, prefix='/api/admin')
app.include_router(calendar.router, prefix='/api/calendar')

@app.get('/api/health')
def health():
    return {'ok': True}
