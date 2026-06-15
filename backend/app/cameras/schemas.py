from pydantic import BaseModel


from uuid import UUID


from typing import Optional







# ----------------------------------
# Create Camera Schema
# ----------------------------------

class CameraCreate(BaseModel):


    name: str


    ip_address: str


    location: str


    rtsp_url: str


    # AI model assigned to camera
    model_id: Optional[int] = None










# ----------------------------------
# Update Camera Schema
# ----------------------------------

class CameraUpdate(BaseModel):


    name: Optional[str] = None


    ip_address: Optional[str] = None


    location: Optional[str] = None


    rtsp_url: Optional[str] = None


    status: Optional[str] = None


    # change assigned AI model
    model_id: Optional[int] = None










# ----------------------------------
# Camera Response Schema
# ----------------------------------

class CameraResponse(BaseModel):


    id: UUID


    name: str


    ip_address: str


    location: str


    rtsp_url: str


    status: str


    connection_status: str


    model_id: Optional[int] = None








    class Config:


        from_attributes = True