from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.tasks.render import render_manim_scene

main_bp = Blueprint("main", __name__)
limiter = Limiter(key_func=get_remote_address)
# Remove this line: csrf = CSRFProtect()

@main_bp.route("/health")
def health_check():
    return jsonify({"status": "healthy"})

@main_bp.route("/render", methods=["POST"])
@limiter.limit("5 per minute")
# Remove @csrf.exempt since we're not using CSRF for APIs
def generate_video():
    data = request.get_json()
    print("data", data)
    if not data or 'code' not in data:
        return jsonify({"error": "No Manim code provided"}), 400
    
    # Basic validation
    code = data['code']
    print(code)
    if len(code) > 10000:  # Reasonable limit
        return jsonify({"error": "Code too long"}), 400
    
    # Enqueue the rendering task
    task = render_manim_scene.delay(code)
    
    return jsonify({
        "task_id": task.id,
        "status": "queued"
    }), 202

@main_bp.route("/status/<task_id>")
def get_task_status(task_id):
    from app.extensions import get_celery_app
    celery_app = get_celery_app()
    task = celery_app.AsyncResult(task_id)
    
    return jsonify({
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.ready() else None
    })
