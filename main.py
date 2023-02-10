import os
import sys
sys.path.insert(
    0, 
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), 
            '..'
        )
    )
)
from dotenv import load_dotenv
from uvicorn import run
from fastapi import FastAPI
from todoApp.config import router
from todoApp.controller import *


app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    load_dotenv()
    run(app, 
        host    =os.getenv('HOST'), 
        port    =int(os.getenv('PORT')), 
        workers =int(os.getenv('WORKERS'))
    )