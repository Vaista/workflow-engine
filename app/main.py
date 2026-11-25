from fastapi import FastAPI
from app.api.routes import ALL_ROUTERS
from app.exceptions import register_exception_handlers


app = FastAPI()


for router in ALL_ROUTERS:
    app.include_router(router)


register_exception_handlers(app)
