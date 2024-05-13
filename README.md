# HW1: Technology Template Repository (Python)
---
### Team Umbreon Members
* Jeevan Vasanthan
* Jimmy Shong
* Jordi Del Castillo
* Mudit Nigam
* Savitha Nair
* Tahmid Asif
---
### About
The primary goal of the “Google Suit Task Manager” is to develop an automated system that can not only efficiently sync with the preexisting Google Suite products but also identify, aggregate, and display tasks across the Google Suite. Furthermore, the main objective is to provide a platform that will allow users to perform all basic task management actions currently available in Google Tasks, including creating tasks, deadlines, and notifications, as well as consolidating these scattered tasks into a consistent, well-defined format, which will increase user productivity and task management efficiency.

---
### Features
* User login and view account
* Aggregate and display all tasks on the task dashboard
* Create tasks and respective deadlines
* View tasks linked to comments/mentions across Google Suite Products
* Sync and integrate with appropriate Google Suite products, including Google Docs, Sheets, Slides, Gmail, and Google Calendar
---
### Demo Video
https://github.com/nyuoss/google-suite-task-manager/assets/33367258/565859d7-d6f3-4d27-af3d-47eb7d99d11c

---
### Installation
1. Create a template using this repository
2. Clone the repository
```
git clone https://github.com/OpenSource-Spring2024/python-template.git
```
3. Create a new Google API project at  https://console.cloud.google.com/.
4. Enable Google Drive API and Google Tasks API
5. Configure Oauth by adding your emails as a test user
6. Get credentials by creating a new OAuth 2.0 Client ID, and make sure your redirect URIs includes http://127.0.0.1:5000/callback.
7. Create a secret key.
8. Configure .env file in app directory. 
```
REACT_APP_CLIENT_ID="Client ID"
REACT_APP_CLIENT_SECRET="Client secret"
```
9. Install dependencies using pdm
```
pdm install
```
10. Turn on your MongoDB service, make sure it configured to localhost:27017.
11.  Run app
```
pdm run flask run
```
12. Click on the link created by Flask or visit 127.0.0.1:5000
13. Press the sign-in with Google login button and log in using a valid Google account.
14. If this is is your first time. you will asked for  additional access to your Google Account. Check the Select All.
15. Start using the web app!
---
## Usage Instructions
   - On Tasks homepage users can perform all basic task management actions available in Google Tasks, including creating, fetching and deleting tasks, add deadlines, and notifications and can sync and integrate with appropriate Google Suite products, like Google Docs.
   - To add tasks, enter task details and the click 'Add tasks'.
   - To aggregate and display all the tasks currently in Google Tasks, click 'Fetch tasks'.
   - To remove a task from Google Tasks, simply click on the "Delete" button located adjacent to the task.
   - To aggregate and display all the comments you are tagged in, click 'Fetch Comments'.

## Contribution Guidelines

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

### Reporting Bugs
- We have multiple GitHub Issues templates, use those to report bugs.
- Before submitting a bug report, please look through old issues to ensure there is no preexisting solution.
- Provide clear steps to reproduce the bugs, and expected vs actual behavior.

### New Features
- Please create a branch from master or fork your own repository
- Any help with managing issues and PRs is very appreciated!
- Write good commit messages.
- There are no strict rules for the code style, but try to follow the patterns in the code (indentation, spaces, etc.). Vertical alignment makes things more readable and easier to batch edit
- Before submitting a PR, please run the unit tests, static type checkers, and code linters.
  - Run unit tests using pytest
      ```
      pdm run pytest
      ```
  - Perform static analysis using mypy
      ```
      pdm run mypy .
      ```
  - Perform code formatting using Ruff
      ```
      pdm run ruff check .
      pdm run ruff format .
      ```
- Add all new packages into pdm.
```
pdm add <package name>
```
- Also update requirements.txt to ensure circleci completes
```
pdm export -o requirements.txt --without-hashes
```