import pytest
from main import app
from test.conftest import (
    test_client,
    get_headers,
    test_user,
    notes,
    delete_user_notes,
    setup_and_teardown_db
)
from utils.enums import NoteLimits
from utils.logger import logger


async def test_read_notes_empty_db(setup_and_teardown_db, test_client, test_user, ):
    headers = await get_headers(test_user)
    response = await test_client.get("/notes/", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


async def test_read_notes(test_client, test_user, notes):
    headers = await get_headers(test_user)
    response = await test_client.get("/notes/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == len(notes)


async def test_create_note(test_client, test_user):
    headers = await get_headers(test_user)
    note_data = {
        "title": "Test Note",
        "description": "This is a test note."
    }
    response = await test_client.post("/notes/", json=note_data, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == note_data["title"]
    assert data["description"] == note_data["description"]


async def test_create_too_many_notes_error(test_client, test_user):
    await delete_user_notes(test_user)
    headers = await get_headers(test_user)

    # Creating notes before reaching the limit should be successful.
    note_data = {"title": "Test Note",
                 "description": "This is a test note."}
    for _ in range(NoteLimits.MAX_NOTES_PER_USER.value):
        response = await test_client.post("/notes/", json=note_data, headers=headers)
        assert response.status_code == 201  # Успешное создание заметки

    # An attempt to create a note exceeding the limit should cause an error.
    note_data = {"title": "One Too Many",
                 "description": "This note should not be created."}
    response = await test_client.post("/notes/", json=note_data, headers=headers)

    # Checking that the status 400 and error message are returned.
    assert response.status_code == 400
    assert NoteLimits.TOO_MANY_NOTES_ERROR_MSG.value in response.json().get("detail", "")
    await delete_user_notes(test_user)


async def test_create_note_with_incorrect_title(test_client, test_user):
    headers = await get_headers(test_user)
    note_data = {"title": "Te",
                 "description": "This is a test note with incorrect title."}
    response = await test_client.post("/notes/", json=note_data, headers=headers)

    assert response.status_code == 422
    text_error = "The course title must be at least 3 characters long."
    assert text_error in response.json().get("detail", "")[0].get("msg", "")


async def test_read_note(test_client, test_user, notes):
    test_note = notes[0]
    headers = await get_headers(test_user)
    response = await test_client.get(f"/notes/{test_note.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_note.id
    assert data["title"] == test_note.title
    assert data["description"] == test_note.description


async def test_update_note(test_client, test_user, notes):
    test_note = notes[0]
    headers = await get_headers(test_user)

    update_data = {"title": "Updated Title",
                   "description": "Updated Description"}

    response = await test_client.put(f"/notes/{test_note.id}", json=update_data, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]


async def test_delete_note(test_client, test_user, notes):
    test_note = notes[0]
    headers = await get_headers(test_user)

    response = await test_client.delete(f"/notes/{test_note.id}", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_note.id

    # Check that the note is really deleted
    response = await test_client.get(f"/notes/{test_note.id}", headers=headers)
    assert response.status_code == 404
