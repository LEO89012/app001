FastAPI backend (SQLite) for MedAgenda
=====================================

Setup (recommended in a virtualenv):

    python -m venv .venv
    source .venv/bin/activate    # Windows: .venv\Scripts\activate
    pip install -r requirements.txt

Crear la base de datos y poblarla:

    python seed_db.py

Correr servidor:

    uvicorn main:app --reload --port 8000

Arquitectura:
- main.py: instancia FastAPI y rutas
- models.py: modelos SQLModel
- crud.py: funciones de acceso a datos
- auth.py: JWT auth helpers
- routers/: endpoints modularizados
- uploads/: carpeta para PDFs


# Tests

Run tests:

```
pytest
```

CI workflows are included in .github/workflows


## HTTPS & Secrets (production)

- Use environment variables (e.g. in Render, Fly, Heroku) to store secrets: `JWT_SECRET`, `DATABASE_URL`, `SMTP_*`, `TWILIO_*`.
- For local HTTPS testing with uvicorn:

```
uvicorn main:app --host 0.0.0.0 --port 443 --ssl-keyfile=/path/to/key.pem --ssl-certfile=/path/to/cert.pem
```

- Rotate keys periodically: maintain key identifiers and automate rotation by using a secrets manager (AWS Secrets Manager, Google Secret Manager, HashiCorp Vault). Avoid hardcoding secrets in code.
- Use monitoring and alerting for failed login attempts and unusual email/SMS volumes.
