from fastapi import FastAPI
from app.routers import tables
from app.routers import reservations

app = FastAPI()
app.include_router(tables.router)
app.include_router(reservations.router)

@app.get("/")
def read_root():
    return {"message": "Hello from restaurant_booking"}


