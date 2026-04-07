from fastapi import FastAPI
from app.middlewares.request_time import get_request_time
from app.routers import blog, tag, user

# App instance
app = FastAPI()

# Middlewares
app.middleware('http')(get_request_time)

# Routes
app.include_router(user.router)
app.include_router(blog.router)
app.include_router(tag.router)
