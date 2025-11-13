from fastapi import FastAPI
from search.router import router


app = FastAPI()

app.include_router(router, prefix="/api")
