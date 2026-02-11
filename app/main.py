from fastapi import FastAPI
from app.middlewares.request_time import get_request_time
from app.routers import user

# App instance
app = FastAPI()

# Middlewares
app.middleware('http')(get_request_time)

# Routes
app.include_router(user.router)
