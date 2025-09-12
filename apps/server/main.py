from fastapi import FastAPI
from prisma import Prisma

db = Prisma()

app = FastAPI()

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

# GET /
@app.get("/analyses")
async def get_analyses():
    """Fetch all Analysis records from the database."""
    results = await db.analysis.find_many()
    return results

# GET /
@app.get("/")
async def index():
    return {"Message": "Hello World, from FastAPI!"}