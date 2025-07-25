from flask import Flask
from .extensions import cors, limiter, celery_init_app
from .routes.main import main_bp

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['CELERY'] = {
        'broker_url': 'redis://localhost:6379/0',
        'result_backend': 'redis://localhost:6379/0'
    }
    
    # Initialize extensions
    # csrf.init_app(app)
    cors.init_app(app)
    limiter.init_app(app)
    celery_init_app(app)
    
    # Register blueprints
    app.register_blueprint(main_bp, url_prefix="/api")
    
    return app
