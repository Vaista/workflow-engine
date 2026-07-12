from fastapi import FastAPI
from app.api.routes import ALL_ROUTERS
from app.exceptions import register_exception_handlers


app = FastAPI()

# app.include_router(health.router, prefix="/health", tags=["Health"])
# app.include_router(users.router, prefix="/users", tags=["Users"])
# app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

for router in ALL_ROUTERS:
    app.include_router(router['router'], prefix=f"/{router['prefix']}", tags=[f"{router['tag']}"])


register_exception_handlers(app)
