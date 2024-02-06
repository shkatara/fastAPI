
# API Builder using Python FastAPI

The Project is to create a fully functional API with a working MySQL Database to implement the following operations: 

1. Create
2. Read
3. Update
3. Delete

\
This project serves as a self learning to have a better understanding of APIs. The project implements the API with a fully functional JWT token authentication mechanism, have all the correct response and status codes depending on the actual status of the code execution.

Along the way of this project, it uses:
1. Python 3.9.6 (Obviously)
1. FastAPI
2. Pydantic - For setting models for User Input and Responses
3. SQLAlchemy

\
This uses SQLAlchemy as an OMR to take away all the pain of interacting with the database using default SQL statememts and allows python to interact with the database as native functions. It still uses the SQL statements under the hood.

ReadMe created from https://readme.so/editor
## Installation

Install the project with pip. I recommend using python a virtual environment. Any changes to the code will result on a real-time reload of the uvicron engine and the changes are reflected in real time.

```bash
    python -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt
    python app/main.py

```