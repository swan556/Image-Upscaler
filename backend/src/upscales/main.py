from fastapi.middleware.cors import CORSMiddleware
from src.upscales.routers import images, users
from fastapi import FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(images.router)
app.include_router(users.router)