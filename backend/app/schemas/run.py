from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime

class RunBase(BaseModel):
    url: HttpUrl
    figma_link: Optional[str] = None
    project_id: Optional[str] = None

class RunCreate(RunBase):
    pass # Can accept reference image as FileUpload separately

class RunUpdate(BaseModel):
    status: Optional[str] = None
    screenshot_path: Optional[str] = None
    diff_image_path: Optional[str] = None
    issues: Optional[List[Dict[str, Any]]] = None
    score: Optional[float] = None

class RunResponse(RunBase):
    id: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    screenshot_path: Optional[str] = None
    diff_image_path: Optional[str] = None
    issues: Optional[List[Dict[str, Any]]] = None
    score: Optional[float] = None
    
    reference_image_path: Optional[str] = None

    class Config:
        from_attributes = True
