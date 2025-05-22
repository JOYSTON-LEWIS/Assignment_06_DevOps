import pytest
from app import app, students_collection
from bson import ObjectId

# Fixture to create a test client
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Fixture to track and delete only inserted test records
@pytest.fixture
def cleanup_test_records():
    inserted_ids = []
    yield inserted_ids  # Pass list to test
    for _id in inserted_ids:
        students_collection.delete_one({"_id": ObjectId(_id)})

# Test: Add a student
def test_add_student(client, cleanup_test_records):
    response = client.post('/students', json={"name": "Bob"})
    assert response.status_code == 201
    assert response.json["name"] == "Bob"
    cleanup_test_records.append(response.json["_id"])

# Test: Get all students
def test_get_all_students(client, cleanup_test_records):
    result = students_collection.insert_one({"name": "TestUser", "assignedQuestions": "Q1"})
    cleanup_test_records.append(str(result.inserted_id))
    response = client.get('/students')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert any(student["name"] == "TestUser" for student in response.json)

# Test: Get student by name
def test_get_student_by_name(client, cleanup_test_records):
    result = students_collection.insert_one({"name": "Alice", "assignedQuestions": "Q2"})
    cleanup_test_records.append(str(result.inserted_id))
    response = client.get('/students/name/Alice')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[0]["name"] == "Alice"

# Test: Partial name search
def test_get_student_by_partial_name(client, cleanup_test_records):
    result = students_collection.insert_one({"name": "Alice", "assignedQuestions": ""})
    cleanup_test_records.append(str(result.inserted_id))
    response = client.get('/students/name/Ali')
    assert response.status_code == 200
    assert any("Alice" in s["name"] for s in response.json)

# Test: Name not found
def test_get_student_by_name_not_found(client):
    response = client.get('/students/name/NonExistentName')
    assert response.status_code == 404
    assert response.json["error"] == "No students found with the given name"

# Test: Delete student
def test_delete_student(client, cleanup_test_records):
    result = students_collection.insert_one({"name": "Charlie", "assignedQuestions": ""})
    student_id = str(result.inserted_id)
    response = client.delete(f'/students/{student_id}')
    assert response.status_code == 200
    assert response.json["message"] == "Deleted"

    # Ensure it's deleted
    response = client.get(f'/students/{student_id}')
    assert response.status_code == 404

# Test: Add student missing 'name'
def test_add_student_missing_fields(client):
    response = client.post('/students', json={"assignedQuestions": "Q5"})
    assert response.status_code == 400
    assert response.json["error"] == "Missing 'name'"
