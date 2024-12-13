from fastapi import FastAPI
from app.api.routes import candidatos, upload

from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')


app = FastAPI(title="Resume Upload API")

app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])
app.include_router(candidatos.router, prefix="/api/v1/candidatos", tags=["Candidatos"])

@app.get("/")
async def root():
    return {"message": "API IS RUNNING!"}
