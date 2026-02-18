import fastapi

from app.routers import users

app = fastapi.FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(users.router)