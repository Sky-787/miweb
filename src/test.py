from fastapi.testclient import TestClient
from main import app, calculator

client = TestClient(app)

def test_sum():
    calc = calculator()
    assert calc.sum(2, 2) == 4

def test_resta():
    calc = calculator()
    assert calc.resta(5, 3) == 2

# def test_get_tags_is_disabled_by_default():
#     response = client.get("/tags/")
#     assert response.status_code == 403

# def test_create_tag_is_disabled_by_default():
#     response = client.post("/tags/?name=Urgent&color=red")
#     assert response.status_code == 403

def test_create_task_without_tag():
    response = client.post("/tasks/?title=Buy milk")
    assert response.status_code == 200
    assert response.json()["title"] == "Buy milk"
    assert response.json()["tag_id"] is None

# def test_create_task_with_tag_disabled_by_default():
#     response = client.post("/tasks/?title=Buy milk&tag_id=1", headers={"user-id": "123"})
#     assert response.status_code == 403

def test_get_tasks_filtered_by_tag():
    # Insertamos algunas tareas falsas en memoria para probar
    from main import tasks_db
    tasks_db.clear()
    tasks_db.append({"id": 1, "title": "A", "tag_id": 1})
    tasks_db.append({"id": 2, "title": "B", "tag_id": None})
    tasks_db.append({"id": 3, "title": "C", "tag_id": 1})
    
    response = client.get("/tasks/?tag_id=1")
    assert response.status_code == 200
    filtered_tasks = response.json()
    assert len(filtered_tasks) == 2
    assert all(t["tag_id"] == 1 for t in filtered_tasks)