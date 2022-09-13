# FastAPI first tutorial project

Simple API for crud of blog with user authentication.

https://dev.to/sarthaksavvy/fastapi-4-hours-free-course-5cgg

## Technology:

- Python 3.10
- FastAPI
- SQLAlchemy
- OAuth2
- SQLite

### .env file template

```
SECRET_KEY = # project secret key
ALGORITHM = "HS256"
```

## Installation

 - Clone the repository
 - Create `.env` file in project directory
 - Create and activate virtual environment:
```
python3.10 -m venv venv
source venv/bin/activate
```
 
- Install all required packages from requirements.txt:
```
pip install --upgrade pip
pip install -r requirements.txt
```

- Run the project:

`uvicorn blog.main:app --reload `

## Documentation

http://localhost:8000/docs

http://localhost:8000/redoc
