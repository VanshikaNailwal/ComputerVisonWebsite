from fastapi import (

    APIRouter,

    Depends

)



from sqlalchemy.orm import Session



from app.database import get_db



from app.permissions.schemas import PermissionResponse



from app.permissions.service import get_all_permissions







router = APIRouter(

    prefix="/permissions",

    tags=["Permissions"]

)











@router.get(

    "",

    response_model=list[PermissionResponse]

)

def permissions(

    db:Session = Depends(get_db)

):



    permissions = get_all_permissions(

        db

    )





    return [

        {

            "id":str(permission.id),

            "name":permission.name,

            "description":permission.description

        }


        for permission in permissions

    ]