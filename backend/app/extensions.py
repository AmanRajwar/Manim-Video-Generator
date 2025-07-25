from celery import Celery, Task
from flask_limiter import Limiter
# from flask_wtf import CSRFProtect
from flask_cors import CORS

# csrf = CSRFProtect()
cors = CORS()
limiter = Limiter(key_func=lambda: "global")

def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.import_name)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.Task = FlaskTask
    app.extensions["celery"] = celery_app
    return celery_app
