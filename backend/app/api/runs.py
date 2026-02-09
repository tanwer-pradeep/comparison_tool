from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import uuid
import shutil
import os

from app.core.database import get_db
from app.models.run import Run
from app.schemas.run import RunResponse
from app.worker import process_run
from app.core.config import settings

router = APIRouter()

@router.post("/", response_model=RunResponse)
async def create_run(
    url: str = Form(...),
    figma_link: Optional[str] = Form(None),
    reference_image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    run_id = str(uuid.uuid4())
    reference_path = None
    
    # Save reference image if provided
    if reference_image:
        os.makedirs(settings.ARTIFACTS_DIR, exist_ok=True)
        file_ext = reference_image.filename.split('.')[-1]
        reference_path = f"{settings.ARTIFACTS_DIR}/{run_id}_ref.{file_ext}"
        with open(reference_path, "wb") as buffer:
            shutil.copyfileobj(reference_image.file, buffer)
    
    new_run = Run(
        id=run_id,
        url=url,
        figma_link=figma_link,
        reference_image_path=reference_path,
        status="pending"
    )
    
    db.add(new_run)
    await db.commit()
    await db.refresh(new_run)
    
    # Trigger Celery Task
    process_run.delay(run_id)
    
    return new_run

@router.get("/{run_id}", response_model=RunResponse)
async def get_run(run_id: str, db: AsyncSession = Depends(get_db)):
    run = await db.get(Run, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run
