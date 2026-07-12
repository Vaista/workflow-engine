from app.api.routes.auth import router as auth_router
from app.api.routes.health import router as health_router
from app.api.routes.users import router as users_router
# from app.api.routes.workflows import workflows_router
# from app.api.routes.workflow_steps import workflow_steps_router
# from app.api.routes.regions import regions_router



ALL_ROUTERS = [
    {
        'router': auth_router,
        'prefix': 'auth',
        'tag': 'Authentication'
    },
    {
        'router': health_router,
        'prefix': 'health',
        'tag': 'Health'
    },
    {
        'router': users_router,
        'prefix': 'users',
        'tag': 'Users'
    },
]