from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routes import user, auth, property, category
from fastapi.staticfiles import StaticFiles

origin = ['*']

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/user_media", StaticFiles(directory="user_media"), name="user_media")
app.mount("/property_media", StaticFiles(directory="property_media"), name="property_media")


class Route:
    def __init__(self, *args) -> None:
        [app.include_router(keys.router) for keys in args]


@app.get('/')
def root():
    return {'message': 'Welcome'}


app_route = Route(user, auth, property, category)

# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

