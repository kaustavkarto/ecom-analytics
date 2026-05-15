from fastapi import FastAPI
from app.api.routes import orders, events

app = FastAPI(
    title="E-Commerce Order Analytics API",
    description="Backend API for order management and analytics",
    version="1.0.0"
)

app.include_router(orders.router)
app.include_router(events.router)

@app.get("/")
def root():
    return {"message": "E-Commerce Analytics API is running"}