from app.exceptions.handlers.workflows import register_workflow_handlers
from app.exceptions.handlers.regions import register_region_handler
from app.exceptions.handlers.organizations import register_organization_handlers


def register_exception_handlers(app):

    register_workflow_handlers(app)
    register_region_handler(app)
    register_organization_handlers(app)
