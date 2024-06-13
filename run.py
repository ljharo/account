# run.py

from uvicorn import run

from app.settings import SERVER_INFO

if __name__ == '__main__':
    
    run(
        **SERVER_INFO
    )