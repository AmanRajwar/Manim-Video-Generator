from celery import shared_task
import tempfile
import uuid
import os
import subprocess

@shared_task(ignore_result=False, time_limit=300)
def render_manim_scene(scene_code: str):
    """Render a Manim scene and return the video path"""
    try:
        # Generate unique ID for this render
        job_id = uuid.uuid4().hex
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(scene_code)
            temp_file = f.name
        
        # Create output directory
        output_dir = f"/tmp/manim_output_{job_id}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Run Manim command
        cmd = [
            "manim", 
            temp_file, 
            "-qm",  # medium quality
            "--output_file", f"scene_{job_id}.mp4"
        ]
        
        result = subprocess.run(
            cmd, 
            cwd=output_dir,
            capture_output=True, 
            text=True, 
            timeout=300
        )
        
        if result.returncode == 0:
            # Move video to static directory (you'll need to create this)
            video_path = f"static/videos/scene_{job_id}.mp4"
            # Implementation for moving file would go here
            return {"success": True, "video_path": video_path}
        else:
            return {"success": False, "error": result.stderr}
            
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        # Clean up temp file
        if 'temp_file' in locals():
            os.unlink(temp_file)
