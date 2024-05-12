# HW1: Technology Template Repository (Python)
---
### Team Umbreon members :
* Jeevan Vasanthan
* Jimmy Shong
* Jordi Del Castillo
* Mudit Nigam
* Savitha Nair
* Tahmid Asif
---
### Installation :
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
### Features :
* Programming language - Python
* Toolchain / runtime environment - Python 3.11
* Testing framework is selected - pytest
* Continuous integration solution - CircleCI
* Static analysis solution - mypy
* Code formatting solution - Ruff
* Package manager - Python Dependency Management
* License - MIT
---
### Objectives Satisfied :
:white_check_mark: Template git repo is created <br>
:white_check_mark: “Hello World” program [main.py](https://github.com/OpenSource-Spring2024/python-template/blob/master/src/main.py)<br> 
:white_check_mark: A test in the repo asserting 2 + 2 == 4 [test_1.py](https://github.com/OpenSource-Spring2024/python-template/blob/master/tests/test_1.py)<br>
:white_check_mark: A Circle CI pipeline that executes the test [config.yml](https://github.com/OpenSource-Spring2024/python-template/blob/master/.circleci/config.yml)<br>
:white_check_mark: A comprehensive README.md file <br>
:white_check_mark: An appropriate .gitignore [.gitignore](https://github.com/OpenSource-Spring2024/python-template/blob/master/.gitignore)<br>
:white_check_mark: An appropriate license [MIT License](https://github.com/OpenSource-Spring2024/python-template/blob/master/LICENSE)<br>
:white_check_mark: Created two components [backend](https://github.com/OpenSource-Spring2024/python-template/tree/master/src/backend) and [hw1](https://github.com/OpenSource-Spring2024/python-template/tree/master/src/hw1) that interact with each other.<br>
:white_check_mark: Created an issue and pull request template.<br>
 






