from fastapi import (

    APIRouter,

    Depends,

    HTTPException

)



from sqlalchemy.orm import Session



from uuid import UUID




from app.database import get_db



from app.users.models import User



from app.auth.dependencies import get_current_user








from app.cameras.schemas import (

    CameraCreate,

    CameraUpdate,

    CameraResponse

)









from app.cameras.service import (

    create_camera,

    get_all_cameras,

    get_camera_by_id,

    update_camera,

    delete_camera,

    test_camera_connection

)









from app.ai.manager import (

    start_ai_process,

    stop_ai_process,

    get_ai_status

)









router = APIRouter(

    prefix="/cameras",

    tags=["Cameras"]

)









# ----------------------------------
# Admin Permission Check
# ----------------------------------

def admin_required(

    user: User

):


    if user.role.name != "ADMIN":


        raise HTTPException(

            status_code=403,

            detail="Admin access required"

        )










# ----------------------------------
# Add Camera
# ----------------------------------

@router.post(

    "",

    response_model=CameraResponse

)

def add_camera(


    data: CameraCreate,


    db: Session = Depends(get_db),


    current_user: User = Depends(get_current_user)


):


    admin_required(

        current_user

    )




    return create_camera(

        db,

        data,

        current_user

    )












# ----------------------------------
# Get All Cameras
# ----------------------------------

@router.get(

    "",

    response_model=list[CameraResponse]

)

def all_cameras(


    db: Session = Depends(get_db),


    current_user: User = Depends(get_current_user)


):



    return get_all_cameras(

        db

    )












# ----------------------------------
# Test Camera Connection
# ----------------------------------

@router.get(

    "/{camera_id}/test"

)

def test_camera(



    camera_id: UUID,


    db: Session = Depends(get_db),


    current_user: User = Depends(get_current_user)


):


    admin_required(

        current_user

    )




    return test_camera_connection(

        db,

        camera_id

    )














# ----------------------------------
# Get Camera By ID
# ----------------------------------

@router.get(

    "/{camera_id}",

    response_model=CameraResponse

)

def single_camera(



    camera_id: UUID,


    db: Session = Depends(get_db),


    current_user: User = Depends(get_current_user)


):



    return get_camera_by_id(

        db,

        camera_id

    )













# ----------------------------------
# Update Camera
# ----------------------------------

@router.patch(

    "/{camera_id}",

    response_model=CameraResponse

)

def edit_camera(



    camera_id: UUID,


    data: CameraUpdate,


    db: Session = Depends(get_db),


    current_user: User = Depends(get_current_user)


):



    admin_required(

        current_user

    )




    return update_camera(

        db,

        camera_id,

        data

    )












# ----------------------------------
# Delete Camera
# ----------------------------------

@router.delete(

    "/{camera_id}"

)

def remove_camera(



    camera_id: UUID,


    db: Session = Depends(get_db),


    current_user: User = Depends(get_current_user)


):



    admin_required(

        current_user

    )




    return delete_camera(

        db,

        camera_id

    )














# ----------------------------------
# Start AI Detection
# ----------------------------------

@router.post(

    "/{camera_id}/start-ai"

)

def start_ai(


    camera_id: UUID,


    current_user: User = Depends(get_current_user)


):



    admin_required(

        current_user

    )




    return start_ai_process(

        camera_id

    )












# ----------------------------------
# Stop AI Detection
# ----------------------------------

@router.post(

    "/{camera_id}/stop-ai"

)

def stop_ai(



    camera_id: UUID,


    current_user: User = Depends(get_current_user)


):



    admin_required(

        current_user

    )




    return stop_ai_process(

        camera_id

    )












# ----------------------------------
# AI Running Status
# ----------------------------------

@router.get(

    "/ai/status"

)

def ai_status(

    current_user: User = Depends(get_current_user)

):


    return get_ai_status()