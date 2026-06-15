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

BASE_DIR = Path(__file__).resolve().parent.parent.parent


MODEL_DIR = (

    BASE_DIR
    /
    "storage"
    /
    "models"

)



MODEL_DIR.mkdir(

    parents=True,

    exist_ok=True

)









# ----------------------------------
# Upload AI Model
# ----------------------------------

@router.post("/upload")
async def upload_model(


    name: str = Form(...),


    usecase: str = Form(...),


    version: str = Form(...),


    file: UploadFile = File(...),


    db: Session = Depends(get_db)


):




    # only allow YOLO models

    if not file.filename.endswith(".pt"):



        raise HTTPException(

            status_code=400,

            detail="Only .pt model files allowed"

        )










    # check duplicate model

    existing = db.query(

        AIModel

    ).filter(

        AIModel.filename == file.filename

    ).first()








    if existing:



        raise HTTPException(

            status_code=400,

            detail="Model already uploaded"

        )










    # save file

    save_path = MODEL_DIR / file.filename








    with open(

        save_path,

        "wb"

    ) as buffer:



        shutil.copyfileobj(

            file.file,

            buffer

        )












    # create database entry

    new_model = AIModel(



        name=name,


        usecase=usecase,


        version=version,


        filename=file.filename,


        file_path=str(save_path),


        status="CHECKING"


    )









    db.add(

        new_model

    )



    db.commit()



    db.refresh(

        new_model

    )












    # ----------------------------------
    # YOLO Validation
    # ----------------------------------

    try:



        YOLO(

            str(save_path)

        )





        new_model.status = "READY"






    except Exception:



        new_model.status = "FAILED"











    db.commit()



    db.refresh(

        new_model

    )













    return {


        "message": "Model uploaded successfully",


        "id": new_model.id,


        "name": new_model.name,


        "usecase": new_model.usecase,


        "version": new_model.version,


        "filename": new_model.filename,


        "path": new_model.file_path,


        "status": new_model.status


    }

















# ----------------------------------
# Get All AI Models
# ----------------------------------

@router.get("")
def get_models(



    db: Session = Depends(get_db)


):




    models = db.query(

        AIModel

    ).all()










    return [


        {


            "id": model.id,


            "name": model.name,


            "usecase": model.usecase,


            "version": model.version,


            "filename": model.filename,


            "path": model.file_path,


            "status": model.status



        }



        for model in models


    ]
















# ----------------------------------
# Delete AI Model
# ----------------------------------

@router.delete("/{model_id}")
def delete_model(



    model_id: int,


    db: Session = Depends(get_db)


):





    model = db.query(

        AIModel

    ).filter(

        AIModel.id == model_id

    ).first()









    if not model:



        raise HTTPException(

            status_code=404,

            detail="Model not found"

        )










    # delete physical .pt file

    file_path = Path(

        model.file_path

    )







    if file_path.exists():



        file_path.unlink()











    # delete database entry

    db.delete(

        model

    )



    db.commit()










    return {


        "message": "Model deleted successfully"


    }