import json
from typing import Any, Generator
from unittest.mock import ANY, MagicMock, patch

import pytest
from flask.testing import FlaskClient

from app import app


@pytest.fixture
def client() -> Generator[Any, Any, Any]:
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_add_task_no_title(client: FlaskClient) -> None:
    response = client.post("/add_task", data={})
    assert response.status_code == 400
    assert "Task title is required" in response.get_json()["error"]


def test_add_task_no_credentials(client: FlaskClient) -> None:
    with client.session_transaction() as session:
        session.pop("credentials", None)  # This will ensure credentials are not set
    response = client.post("/add_task", data={"title": "New Task"})
    assert response.status_code == 401
    assert "User credentials not found" in response.get_json()["error"]


def test_add_task_successful(client: FlaskClient) -> None:
    # Prepare a fake credentials JSON
    fake_credentials = json.dumps(
        {
            "token": "fake-token",
            "refresh_token": "fake-refresh-token",
            "token_uri": "fake-token-uri",
            "client_id": "fake-client-id",
            "client_secret": "fake-client-secret",
            "scopes": ["https://www.googleapis.com/auth/tasks"],
        }
    )

    # Mock the Google API service
    with patch("app.build") as mock_build:
        # Setup a proper return structure for the mocked method calls
        mock_service = MagicMock()
        mock_tasks = MagicMock()
        mock_insert = MagicMock()
        # Setup chain of method calls
        mock_build.return_value = mock_service
        mock_service.tasks.return_value = mock_tasks
        mock_tasks.insert.return_value = mock_insert
        mock_insert.execute.return_value = {"id": "123", "title": "New Task"}  # Correctly structured dictionary

        # Set up session with valid credentials
        with client.session_transaction() as session:
            session["credentials"] = fake_credentials

        # Post request with a valid title
        response = client.post("/add_task", data={"title": "New Task"})

        # Assertions to verify behavior
        assert response.status_code == 200
        assert response.get_json() == {"success": True, "task": {"id": "123", "title": "New Task"}}

        # Verify that the API was called as expected
        mock_build.assert_called_once_with("tasks", "v1", credentials=ANY)
        mock_tasks.insert.assert_called_once_with(
            tasklist="@default", body={"title": "New Task", "notes": None, "due": None}
        )
        mock_insert.execute.assert_called_once()


def test_delete_task_no_id(client: FlaskClient) -> None:
    with client.session_transaction() as session:
        session["credentials"] = json.dumps({"fake": "credentials"})
    response = client.post("/delete_task", data={})  # No 'id' provided
    assert response.status_code == 400
    assert "Task ID is required" in response.get_json()["error"]


def test_delete_task_no_credentials(client: FlaskClient) -> None:
    response = client.post("/delete_task", data={"id": "123"})
    assert response.status_code == 401
    assert "User credentials not found" in response.get_json()["error"]


def test_delete_task_successful(client: FlaskClient) -> None:
    # Prepare a fake credentials JSON
    fake_credentials = json.dumps(
        {
            "token": "fake-token",
            "refresh_token": "fake-refresh-token",
            "token_uri": "fake-token-uri",
            "client_id": "fake-client-id",
            "client_secret": "fake-client-secret",
            "scopes": ["https://www.googleapis.com/auth/tasks"],
        }
    )
    with patch("app.build") as mock_build:
        mock_service = MagicMock()
        mock_tasks = MagicMock()
        mock_delete = MagicMock()

        mock_build.return_value = mock_service
        mock_service.tasks.return_value = mock_tasks
        mock_tasks.delete.return_value = mock_delete
        mock_delete.execute.return_value = None  # Google API returns None on successful deletion

        # Setup session with valid credentials
        with client.session_transaction() as session:
            session["credentials"] = fake_credentials

        response = client.post("/delete_task", data={"id": "123"})
        assert response.status_code == 200
        assert response.get_json() == {"success": True}


def test_list_tasks_no_credentials(client: FlaskClient) -> None:
    response = client.get("/list_tasks")
    assert response.status_code == 401
    assert "User credentials not found" in response.get_json()["error"]


def test_list_tasks_successful(client: FlaskClient) -> None:
    fake_credentials = json.dumps(
        {
            "token": "fake-token",
            "refresh_token": "fake-refresh-token",
            "token_uri": "fake-token-uri",
            "client_id": "fake-client-id",
            "client_secret": "fake-client-secret",
            "scopes": ["https://www.googleapis.com/auth/tasks"],
        }
    )
    mock_tasks_list = {"items": [{"id": "1", "title": "Task One"}, {"id": "2", "title": "Task Two"}]}

    with patch("app.build") as mock_build:
        mock_service = MagicMock()
        mock_tasks = MagicMock()
        mock_list = MagicMock()

        mock_build.return_value = mock_service
        mock_service.tasks.return_value = mock_tasks
        mock_tasks.list.return_value = mock_list
        mock_list.execute.return_value = mock_tasks_list

        with client.session_transaction() as session:
            session["credentials"] = fake_credentials

        response = client.get("/list_tasks")
        assert response.status_code == 200
        assert response.get_json() == [{"id": "1", "title": "Task One"}, {"id": "2", "title": "Task Two"}]
