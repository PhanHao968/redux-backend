from fastapi import FastAPI
from routes.sim_routes import sim_api_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "redux-frontend.onrender.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sim_api_router)