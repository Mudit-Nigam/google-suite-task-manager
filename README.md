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
### Installation
1. Create a template using this repository
2. Clone the repository
   ```
   git clone https://github.com/OpenSource-Spring2024/python-template.git
   ```
3. Install dependencies using pdm
   ```
   pdm install
   ```
4. Run unit tests using pytest
   ```
   pdm run pytest
   ```
5. Perform static analysis using mypy
   ```
   pdm run mypy .
   ```
6. Perform code formatting using Ruff
   ```
   pdm run ruff check .
   pdm run ruff format .
   ```
7. Run app
   ```
   pdm run flask run
   ```
---
### Technical Specifications
* Programming language - Python
* Toolchain / runtime environment - Python 3.11
* Testing framework is selected - pytest
* Continuous integration solution - CircleCI
* Static analysis solution - mypy
* Code formatting solution - Ruff
* Package manager - Python Dependency Management
* License - MIT

---
### Objectives Satisfied
:white_check_mark: Template git repo is created <br>
:white_check_mark: “Hello World” program [main.py](https://github.com/OpenSource-Spring2024/python-template/blob/master/src/main.py)<br> 
:white_check_mark: A test in the repo asserting 2 + 2 == 4 [test_1.py](https://github.com/OpenSource-Spring2024/python-template/blob/master/tests/test_1.py)<br>
:white_check_mark: A Circle CI pipeline that executes the test [config.yml](https://github.com/OpenSource-Spring2024/python-template/blob/master/.circleci/config.yml)<br>
:white_check_mark: A comprehensive README.md file <br>
:white_check_mark: An appropriate .gitignore [.gitignore](https://github.com/OpenSource-Spring2024/python-template/blob/master/.gitignore)<br>
:white_check_mark: An appropriate license [MIT License](https://github.com/OpenSource-Spring2024/python-template/blob/master/LICENSE)<br>
:white_check_mark: Created two components [backend](https://github.com/OpenSource-Spring2024/python-template/tree/master/src/backend) and [hw1](https://github.com/OpenSource-Spring2024/python-template/tree/master/src/hw1) that interact with each other.<br>
:white_check_mark: Created an issue and pull request template.<br>
 


---
### Demo Video
https://github.com/nyuoss/google-suite-task-manager/assets/33367258/565859d7-d6f3-4d27-af3d-47eb7d99d11c






