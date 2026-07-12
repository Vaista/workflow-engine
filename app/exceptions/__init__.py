from app.exceptions.handlers.workflows import register_workflow_handlers


def register_exception_handlers(app):

    register_workflow_handlers(app)
