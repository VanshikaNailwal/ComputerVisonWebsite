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


router = APIRouter(
    prefix="/models",
    tags=["AI Models"]
)

MODEL_DIR = Path(settings.MODEL_PATH)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


@router.post("/upload")
async def upload_model(
    name: str = Form(...),
    usecase: str = Form(...),
    version: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename.endswith(".pt"):
        raise HTTPException(
            status_code=400,
            detail="Only .pt model files allowed"
        )

    existing = (
        db.query(AIModel)
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

    model_save_path = MODEL_DIR / file.filename

    with open(model_save_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    new_model = AIModel(
        name=name,
        usecase=usecase,
        version=version,
        filename=file.filename,
        file_path=file.filename,
        status="CHECKING"
    )

    db.add(new_model)
    db.commit()
    db.refresh(new_model)

    try:
        YOLO(str(model_save_path))
        new_model.status = "READY"

    except Exception:
        new_model.status = "FAILED"

    db.commit()
    db.refresh(new_model)

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


@router.get("")
def get_models(
    db: Session = Depends(get_db)
):

    models = (
        db.query(AIModel)
        .all()
    )

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


@router.delete("/{model_id}")
def delete_model(
    model_id: int,
    db: Session = Depends(get_db)
):

    model = (
        db.query(AIModel)
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

    db.query(Event).filter(
        Event.model_id == model.id
    ).update(
        {
            Event.model_id: None
        }
    )

    model_file = MODEL_DIR / model.filename

    if model_file.exists():
        model_file.unlink()

    db.delete(model)
    db.commit()

    return {
        "message": "Model deleted successfully"
    }