from fastapi import (

    APIRouter,

    Depends

)



from sqlalchemy.orm import Session



from uuid import UUID





from app.database import get_db



from app.mapping.schemas import (

    MappingCreate,

    MappingResponse

)



from app.mapping.service import (

    create_mapping,

    get_all_mappings,

    delete_mapping

)












# ----------------------------------
# Router
# ----------------------------------

router = APIRouter(

    prefix="/mapping",

    tags=["Camera Model Mapping"]

)













# ----------------------------------
# Create / Update Mapping
# ----------------------------------

@router.post(

    ""

)

def add_mapping(


    data: MappingCreate,


    db: Session = Depends(get_db)


):



    return create_mapping(

        db,

        data

    )















# ----------------------------------
# Get All Mapping
# ----------------------------------

@router.get(

    "",

    response_model=list[MappingResponse]

)

def get_mapping(


    db: Session = Depends(get_db)


):



    return get_all_mappings(

        db

    )















# ----------------------------------
# Delete Camera Mapping
# ----------------------------------

@router.delete(

    "/{camera_id}"

)

def remove_mapping(


    camera_id: UUID,


    db: Session = Depends(get_db)


):



    return delete_mapping(

        db,

        camera_id

    )