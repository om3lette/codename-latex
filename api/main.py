from fastapi import FastAPI
from api.render import latex_router

app: FastAPI = FastAPI()

app.include_router(latex_router, prefix='/latex')
