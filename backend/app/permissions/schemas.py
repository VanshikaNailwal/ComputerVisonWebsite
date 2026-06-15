from pydantic import BaseModel







class PermissionResponse(BaseModel):


    id: str


    name: str


    description: str | None = None