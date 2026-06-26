from pathlib import Path


from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException
)


from sqlalchemy.orm import Session


import shutil


from ultralytics import YOLO



from app.database import get_db


from app.ai_models.models import AIModel


from app.events.models import Event


from app.core.config import settings







# ----------------------------------
# Router
# ----------------------------------

router = APIRouter(

    prefix="/models",

    tags=["AI Models"]

)







# ----------------------------------
# Model Storage Directory
# ----------------------------------

MODEL_DIR = Path(

    settings.MODEL_PATH

)


MODEL_DIR.mkdir(

    parents=True,

    exist_ok=True

)










# ----------------------------------
# Upload AI Model + Logic File
# ----------------------------------

@router.post("/upload")
async def upload_model(


    name: str = Form(...),


    usecase: str = Form(...),


    version: str = Form(...),


    file: UploadFile = File(...),


    logic_file: UploadFile = File(...),


    db: Session = Depends(get_db)


):



    # ------------------------------
    # Validate YOLO file
    # ------------------------------

    if not file.filename.endswith(".pt"):


        raise HTTPException(

            status_code=400,

            detail="Only .pt model files allowed"

        )







    # ------------------------------
    # Validate logic file
    # ------------------------------

    if not logic_file.filename.endswith(".py"):


        raise HTTPException(

            status_code=400,

            detail="Only .py logic files allowed"

        )










    # ------------------------------
    # Duplicate model check
    # ------------------------------

    existing = (

        db.query(

            AIModel

        )

        .filter(

            AIModel.filename == file.filename

        )

        .first()

    )




    if existing:


        raise HTTPException(

            status_code=400,

            detail="Model already uploaded"

        )









    # ------------------------------
    # Save .pt file
    # ------------------------------

    model_save_path = (

        MODEL_DIR

        /

        file.filename

    )



    with open(

        model_save_path,

        "wb"

    ) as buffer:


        shutil.copyfileobj(

            file.file,

            buffer

        )









    # ------------------------------
    # Save .py logic file
    # ------------------------------

    logic_save_path = (

        MODEL_DIR

        /

        logic_file.filename

    )



    with open(

        logic_save_path,

        "wb"

    ) as buffer:


        shutil.copyfileobj(

            logic_file.file,

            buffer

        )









    # ------------------------------
    # Database Entry
    # ------------------------------

    new_model = AIModel(


        name=name,


        usecase=usecase,


        version=version,


        filename=file.filename,


        file_path=file.filename,


        logic_filename=logic_file.filename,


        logic_path=logic_file.filename,


        status="CHECKING"

    )







    db.add(

        new_model

    )


    db.commit()


    db.refresh(

        new_model

    )









    # ------------------------------
    # Validate YOLO model
    # ------------------------------

    try:


        YOLO(

            str(model_save_path)

        )



        new_model.status="READY"




    except Exception:


        new_model.status="FAILED"






    db.commit()


    db.refresh(

        new_model

    )










    return {


        "message":"Model uploaded successfully",


        "id":new_model.id,


        "name":new_model.name,


        "usecase":new_model.usecase,


        "version":new_model.version,


        "filename":new_model.filename,


        "path":new_model.file_path,


        "logic_filename":new_model.logic_filename,


        "logic_path":new_model.logic_path,


        "status":new_model.status

    }













# ----------------------------------
# Get All Models
# ----------------------------------

@router.get("")
def get_models(


    db: Session = Depends(get_db)


):


    models = (

        db.query(

            AIModel

        )

        .all()

    )






    return [


        {


            "id":model.id,


            "name":model.name,


            "usecase":model.usecase,


            "version":model.version,


            "filename":model.filename,


            "path":model.file_path,


            "logic_filename":model.logic_filename,


            "logic_path":model.logic_path,


            "status":model.status


        }


        for model in models


    ]












# ----------------------------------
# Delete AI Model
# ----------------------------------

@router.delete("/{model_id}")
def delete_model(


    model_id:int,


    db: Session = Depends(get_db)


):




    model = (

        db.query(

            AIModel

        )

        .filter(

            AIModel.id == model_id

        )

        .first()

    )







    if not model:


        raise HTTPException(

            status_code=404,

            detail="Model not found"

        )










    # ------------------------------
    # Remove alert references
    # ------------------------------

    db.query(

        Event

    ).filter(

        Event.model_id == model.id

    ).update(

        {

            Event.model_id:None

        }

    )










    # ------------------------------
    # Delete .pt file
    # ------------------------------

    model_file = (

        MODEL_DIR

        /

        model.filename

    )



    if model_file.exists():


        model_file.unlink()









    # ------------------------------
    # Delete .py logic file
    # ------------------------------

    if model.logic_filename:


        logic_file = (

            MODEL_DIR

            /

            model.logic_filename

        )



        if logic_file.exists():


            logic_file.unlink()










    db.delete(

        model

    )


    db.commit()









    return {


        "message":"Model deleted successfully"


    }