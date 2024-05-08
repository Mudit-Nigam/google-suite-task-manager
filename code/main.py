import os
import pathlib
import json
import logging

import requests
from flask import Flask, session, abort, redirect, request, render_template, jsonify
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

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
            "redirect_uris": ["http://localhost/callback"]
        }
    },
    scopes=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/tasks"],
    redirect_uri="http://localhost/callback"
)

@app.route("/add_task", methods=["POST"])
def add_task():
    try:
        task_title = request.form.get("title")
        if not task_title:
            return jsonify({"error": "Task title is required"}), 400

        if "credentials" not in session:
            return jsonify({"error": "User credentials not found"}), 401

        credentials = Credentials.from_authorized_user_info(json.loads(session["credentials"]))

        service = build('tasks', 'v1', credentials=credentials)

        task = {
            'title': task_title
        }

        result = service.tasks().insert(tasklist='@default', body=task).execute()
        return jsonify({"success": True, "task": result})
    except Exception as e:
        logging.error("Error adding task: %s", e)
        return jsonify({"error": "Failed to add task"}), 500

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

# Remaining routes...

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(host='0.0.0.0', port=80, debug=True)
