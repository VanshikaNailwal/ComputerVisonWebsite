from pydantic import BaseModel


from uuid import UUID










# ----------------------------------
# Create Mapping Request
# ----------------------------------

class MappingCreate(BaseModel):


    camera_id: UUID


    model_ids: list[int]












# ----------------------------------
# Single Model Info Response
# ----------------------------------

class ModelInfo(BaseModel):


    id: int


    name: str


    filename: str












# ----------------------------------
# Mapping Response
# ----------------------------------

class MappingResponse(BaseModel):


    camera_id: UUID


    camera_name: str


    models: list[ModelInfo]