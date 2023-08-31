from fastapi import FastAPI
from routes.sim_routes import sim_api_router
from fastapi.middleware.cors import CORSMiddleware

import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()


LOCALHOST = os.getenv("LOCALHOST")
origins = [
    LOCALHOST,
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sim_api_router)