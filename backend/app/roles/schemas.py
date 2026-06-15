from pydantic import BaseModel







# ----------------------------------
# Create Role
# ----------------------------------

class RoleCreate(BaseModel):


    name: str


    description: str | None = None


    permissions: list[str] = []










# ----------------------------------
# Role Response
# ----------------------------------

class RoleResponse(BaseModel):


    id: str


    name: str


    description: str | None


    permissions: list[str]