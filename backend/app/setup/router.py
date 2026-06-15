from fastapi import (

    APIRouter,

    Depends

)



from sqlalchemy.orm import Session



from app.database import get_db



from app.setup.schemas import SuperAdminCreate



from app.setup.service import (

    is_setup_required,

    create_super_admin

)







router = APIRouter(

    prefix="/setup",

    tags=["Setup"]

)






@router.get("/status")

def setup_status(

    db:Session=Depends(get_db)

):


    return {

        "setup_required":

        is_setup_required(db)

    }







@router.post("/create-admin")

def setup_admin(

    data:SuperAdminCreate,


    db:Session=Depends(get_db)

):


    admin=create_super_admin(

        db,

        data

    )


    return {

        "message":"Super admin created",

        "email":admin.email

    }