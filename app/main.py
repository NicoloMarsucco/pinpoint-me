import fastapi

from app.routers import auth

app = fastapi.FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth.router)
