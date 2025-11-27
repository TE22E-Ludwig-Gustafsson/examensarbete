from fastapi import FastAPI
from routers import schedule


app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(schedule.router, prefix ="/api/schedule")