from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_admin_only_create_empresa():
    # try without token - should be unauthorized or forbidden
    r = client.post('/api/admin/empresas', json={'nombre':'X'})
    assert r.status_code in (401,403)
