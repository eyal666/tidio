from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

app = FastAPI()


app.mount("/", StaticFiles(directory="static", html=True), name="static")
