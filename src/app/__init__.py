import json
import logging
import os
import pathlib
from datetime import date, datetime
from typing import Dict, Union

import flask.wrappers as wrappers
import google.auth.transport.requests
import requests
from backend import database as db
from dotenv import load_dotenv
from flask import Flask, abort, jsonify, redirect, render_template, request, session
from google.oauth2 import id_token
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow  # type: ignore
from googleapiclient.discovery import build
from werkzeug.wrappers import Response


load_dotenv()

CLIENT_SECRET = os.getenv("REACT_APP_CLIENT_SECRET")
CLIENT_ID = os.getenv("REACT_APP_CLIENT_ID")

app = Flask(__name__)
app.secret_key = CLIENT_SECRET

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = CLIENT_ID
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_config(
    client_config={
        "web": {
            "client_id": CLIENT_ID,
            "project_id": "your-project-id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": CLIENT_SECRET,
            "redirect_uris": ["http://localhost/callback", "http://127.0.0.1:5000/callback"],
        }
    },
    scopes=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/tasks",
        "https://www.googleapis.com/auth/documents.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ],
    redirect_uri="http://127.0.0.1:5000/callback",
)


@app.route("/add_task", methods=["POST"])
def add_task() -> Union[wrappers.Response, tuple[wrappers.Response, int]]:
    try:
        mydb = db.get_database()
        task_title = request.form.get("title")
        task_notes = request.form.get("notes")
        task_due = request.form.get("due")

        if not task_title:
            return jsonify({"error": "Task title is required"}), 400

        if "credentials" not in session or not session["credentials"]:
            return jsonify({"error": "User credentials not found"}), 401

        credentials = Credentials.from_authorized_user_info(json.loads(session["credentials"]))

        service = build("tasks", "v1", credentials=credentials)
        userinfo_service = build("oauth2", "v2", credentials=credentials)
        user_info = userinfo_service.userinfo().get().execute()
        your_email = user_info.get("email")
        if task_due:
            task_due = task_due + "T23:59"
            date = datetime.strptime(task_due, "%Y-%m-%dT%H:%M").isoformat() + "Z"
            task = (
                {"title": task_title, "notes": task_notes, "due": date}
                if task_notes
                else {"title": task_title, "notes": None, "due": date}  # type: ignore
            )
        else:
            task = (
                {"title": task_title, "notes": task_notes, "due": None}  # type: ignore
                if task_notes
                else {"title": task_title, "notes": None, "due": None}  # type: ignore
            )
        result = service.tasks().insert(tasklist="@default", body=task).execute()  # type: ignore
        db.add_task_db(mydb, result["id"], result["title"], task["notes"], task["due"], your_email)
        print(result)
        return jsonify({"success": True, "task": result})
    except Exception as e:
        logging.error("Error adding task: %s", e)
        return jsonify({"error": "Failed to add task"}), 500


@app.route("/add_task_no_mongo", methods=["POST"])
def add_task_no_mongo() -> Union[wrappers.Response, tuple[wrappers.Response, int]]:
    try:
        task_title = request.form.get("title")
        task_notes = request.form.get("notes")
        task_due = request.form.get("due")

        if not task_title:
            return jsonify({"error": "Task title is required"}), 400

        if "credentials" not in session or not session["credentials"]:
            return jsonify({"error": "User credentials not found"}), 401

        credentials = Credentials.from_authorized_user_info(json.loads(session["credentials"]))

        service = build("tasks", "v1", credentials=credentials)
        userinfo_service = build("oauth2", "v2", credentials=credentials)
        userinfo_service.userinfo().get().execute()
        if task_due:
            task_due = task_due + "T23:59"
            date = datetime.strptime(task_due, "%Y-%m-%dT%H:%M").isoformat() + "Z"
            task = (
                {"title": task_title, "notes": task_notes, "due": date}
                if task_notes
                else {"title": task_title, "notes": None, "due": date}  # type: ignore
            )
        else:
            task = (
                {"title": task_title, "notes": task_notes, "due": None}  # type: ignore
                if task_notes
                else {"title": task_title, "notes": None, "due": None}  # type: ignore
            )
        result = service.tasks().insert(tasklist="@default", body=task).execute()  # type: ignore
        print(result)
        return jsonify({"success": True, "task": result})
    except Exception as e:
        logging.error("Error adding task: %s", e)
        return jsonify({"error": "Failed to add task"}), 500


@app.route("/list_tasks")
def list_tasks() -> Union[wrappers.Response, tuple[wrappers.Response, int]]:
    try:
        mydb = db.get_database()
        if "credentials" not in session:
            return jsonify({"error": "User credentials not found"}), 401

        credentials = Credentials.from_authorized_user_info(json.loads(session["credentials"]))

        service = build("tasks", "v1", credentials=credentials)
        userinfo_service = build("oauth2", "v2", credentials=credentials)
        user_info = userinfo_service.userinfo().get().execute()
        your_email = user_info.get("email")

        # Example: Retrieve tasks from Google Tasks API
        tasks_result = service.tasks().list(tasklist="@default").execute()
        tasks = tasks_result.get("items", [])
        db.update_task_db(mydb, tasks, your_email)
        # Extract tasks from response
        return jsonify(tasks)
    except Exception as e:
        logging.error("Error listing tasks: %s", e)
        return jsonify({"error": "Failed to list tasks"}), 500


@app.route("/list_tasks_no_mongo")
def list_tasks_no_mongo() -> Union[wrappers.Response, tuple[wrappers.Response, int]]:
    try:
        if "credentials" not in session:
            return jsonify({"error": "User credentials not found"}), 401

        credentials = Credentials.from_authorized_user_info(json.loads(session["credentials"]))

        service = build("tasks", "v1", credentials=credentials)
        userinfo_service = build("oauth2", "v2", credentials=credentials)
        userinfo_service.userinfo().get().execute()
        # Example: Retrieve tasks from Google Tasks API
        tasks_result = service.tasks().list(tasklist="@default").execute()
        tasks = tasks_result.get("items", [])
        # Extract tasks from response
        return jsonify(tasks)
    except Exception as e:
        logging.error("Error listing tasks: %s", e)
        return jsonify({"error": "Failed to list tasks"}), 500


@app.route("/delete_task", methods=["POST"])
def delete_task() -> Union[wrappers.Response, tuple[wrappers.Response, int]]:
    try:
        mydb = db.get_database()
        task_id = request.form.get("id")
        if not task_id:
            return jsonify({"error": "Task ID is required"}), 400

        if "credentials" not in session:
            return jsonify({"error": "User credentials not found"}), 401

        credentials = Credentials.from_authorized_user_info(json.loads(session["credentials"]))

        service = build("tasks", "v1", credentials=credentials)
        userinfo_service = build("oauth2", "v2", credentials=credentials)
        user_info = userinfo_service.userinfo().get().execute()
        your_email = user_info.get("email")
        service.tasks().delete(tasklist="@default", task=task_id).execute()
        db.delete_task_db(mydb, task_id, your_email)
        return jsonify({"success": True})
    except Exception as e:
        logging.error("Error deleting task: %s", e)
        return jsonify({"error": "Failed to delete task"}), 500


@app.route("/delete_task_no_mongo", methods=["POST"])
def delete_task_no_mongo() -> Union[wrappers.Response, tuple[wrappers.Response, int]]:
    try:
        task_id = request.form.get("id")
        if not task_id:
            return jsonify({"error": "Task ID is required"}), 400

        if "credentials" not in session:
            return jsonify({"error": "User credentials not found"}), 401

        credentials = Credentials.from_authorized_user_info(json.loads(session["credentials"]))

        service = build("tasks", "v1", credentials=credentials)
        userinfo_service = build("oauth2", "v2", credentials=credentials)
        userinfo_service.userinfo().get().execute()
        service.tasks().delete(tasklist="@default", task=task_id).execute()
        return jsonify({"success": True})
    except Exception as e:
        logging.error("Error deleting task: %s", e)
        return jsonify({"error": "Failed to delete task"}), 500


@app.route("/login")
def login() -> Response:
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback() -> Response:
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    id_token_info = id_token.verify_oauth2_token(
        credentials.id_token, google.auth.transport.requests.Request(), GOOGLE_CLIENT_ID, clock_skew_in_seconds=10
    )

    session["google_id"] = id_token_info.get("sub")
    session["credentials"] = credentials.to_json()
    session["name"] = id_token_info.get("name")
    return redirect("/protected_area")


@app.route("/logout")
def logout() -> Response:
    session.clear()
    return redirect("/")


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/protected_area")
def protected_area() -> str:
    if "google_id" not in session:
        return abort(401)  # Authorization required
    name = session.get("name", "Guest")  # Default value 'Guest' if 'name' key is not found
    return render_template("protected_area.html", name=name)


@app.route("/list_comments")
def list_comments() -> Union[wrappers.Response, tuple[wrappers.Response, int]]:
    try:
        if "credentials" not in session:
            return jsonify({"error": "User credentials not found"}), 401
        credentials = Credentials.from_authorized_user_info(json.loads(session["credentials"]))
        service = build("drive", "v3", credentials=credentials)
        userinfo_service = build("oauth2", "v2", credentials=credentials)
        user_info = userinfo_service.userinfo().get().execute()
        your_email = user_info.get("email")
        # Retrieve files from Google Drive API
        all_files = []
        page_token = None
        while True:
            response = (
                service.files()
                .list(
                    pageSize=100,  # Adjust pageSize as needed
                    fields="nextPageToken, files(id, name, webViewLink, mimeType)",
                    pageToken=page_token,  # type: ignore
                )
                .execute()
            )
            all_files.extend(response.get("files", []))
            page_token = response.get("nextPageToken")

            if not page_token:
                break
        # Retrieve comments from Google Drive API
        result = []
        for file in all_files:
            if "google-apps" in file["mimeType"]:  # Checking if the file type supports comments
                comments = (
                    service.comments()
                    .list(
                        fileId=file["id"],
                        fields="comments(id, author(displayName), content, deleted, resolved)",  # Include 'deleted' and 'resolved' fields
                    )
                    .execute()
                )
                file_comments = comments.get("comments", [])
                relevant_comments = [
                    comment
                    for comment in file_comments
                    if your_email in comment["content"] and not comment.get("deleted") and not comment.get("resolved")  # type: ignore
                ]
                relevant_comments = [
                    {
                        "id": comment["id"],
                        "user": your_email,
                        "author": comment["author"]["displayName"],  # type: ignore
                        "filtered_content": comment["content"].replace("@" + your_email, ""),
                        "file": file["name"],
                        "link": file["webViewLink"],
                        "content": comment["content"],
                    }
                    for comment in relevant_comments
                ]
                if relevant_comments:
                    for comment in relevant_comments:
                        result.append(comment)
        return jsonify(result)
    except Exception as e:
        logging.error("Error listing comments: %s", e)
        return jsonify({"error": "Failed to list comments"}), 500
