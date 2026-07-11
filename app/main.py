from fastapi import FastAPI
from app.api.routes import health, users, auth


app = FastAPI()

app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
