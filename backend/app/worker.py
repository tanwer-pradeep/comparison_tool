from celery import Celery
import asyncio
from app.core.config import settings
from app.services.playwright_service import playwright_service
from app.services.diff_service import diff_service
from app.core.database import AsyncSessionLocal
from app.models.run import Run
import shutil
import os

celery_app = Celery(
    "visual_qa_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.task_routes = {"app.worker.process_run": "main-queue"}

async def run_diff_logic(run_id: str):
    async with AsyncSessionLocal() as db:
        run = await db.get(Run, run_id)
        if not run:
            print(f"Run {run_id} not found")
            return

        run.status = "running"
        await db.commit()
        await db.refresh(run)
        
        try:
            # 1. Capture Screenshot
            screenshot_path = os.path.join(settings.ARTIFACTS_DIR, f"{run_id}_actual.png")
            await playwright_service.capture_screenshot(run.url, screenshot_path)
            
            run.screenshot_path = screenshot_path
            
            # 2. Compare if reference exists
            if run.reference_image_path and os.path.exists(run.reference_image_path):
                diff_output_path = os.path.join(settings.ARTIFACTS_DIR, f"{run_id}_diff.png")
                
                # Run diff logic (sync function called from async - might block event loop but okay for MVP worker)
                # In prod, run in executor
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(None, diff_service.compare_images, screenshot_path, run.reference_image_path, diff_output_path, run_id)
                
                run.diff_image_path = diff_output_path
                run.score = result["score"]
                run.issues = result["issues"]
            
            run.status = "completed"
            await db.commit()
            
        except Exception as e:
            print(f"Error processing run {run_id}: {e}")
            run.status = "failed"
            # run.error = str(e) # Add error field to model if needed
            await db.commit()

@celery_app.task(acks_late=True)
def process_run(run_id: str):
    # Run async logic inside sync celery task
    loop = asyncio.get_event_loop()
    # Create new loop if needed for Celery thread
    try:
        loop.run_until_complete(run_diff_logic(run_id))
    except RuntimeError:
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        new_loop.run_until_complete(run_diff_logic(run_id))
