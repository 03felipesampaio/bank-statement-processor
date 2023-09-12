from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_dummy_test():
    assert True == True