from fastapi import FastAPI
from app.api.routes import health, users, auth
from app.exceptions import register_exception_handlers


app = FastAPI()

app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])


register_exception_handlers(app)
