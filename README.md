To run the code:

python -m venv venv
. venv/bin/activate
pip install "fastapi[all]"
uvicorn app.main:app --reload
