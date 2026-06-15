from pydantic import BaseModel


from uuid import UUID


from datetime import datetime


from typing import Optional







# ----------------------------------
# Event Response
# Sent to React
# ----------------------------------

class EventResponse(BaseModel):


    id: UUID



    camera_id: UUID


    camera_name: Optional[str] = None





    model_id: int


    model_name: Optional[str] = None





    # Detection
    label: str



    confidence: float





    # Evidence
    image_path: Optional[str] = None






    # Alert Status
    status: str





    # Admin Resolution Info
    resolution_note: Optional[str] = None


    resolved_by: Optional[str] = None


    resolved_at: Optional[datetime] = None






    # Created
    created_at: datetime






    class Config:


        from_attributes = True







# ----------------------------------
# Update Status Request
# ACTIVE -> RESOLVED/FALSE ALARM
# ----------------------------------

class EventStatusUpdate(BaseModel):


    status: str


    resolution_note: str


    resolved_by: Optional[str] = None