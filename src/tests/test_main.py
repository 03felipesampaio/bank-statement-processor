from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def dummy_test():
    assert True == True