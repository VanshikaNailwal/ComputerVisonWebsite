from pathlib import Path

import asyncio

import logging

from contextlib import asynccontextmanager



from fastapi import (

    FastAPI,

    Depends

)



from fastapi.middleware.cors import CORSMiddleware


from fastapi.staticfiles import StaticFiles


from fastapi.responses import FileResponse



from sqlalchemy.orm import Session


from sqlalchemy import text





from app.core.config import settings



from app.database import (

    get_db,

    SessionLocal

)









# ----------------------------------
# Logging
# ----------------------------------

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)



logger = logging.getLogger(

    __name__

)









# ----------------------------------
# Import Models
# ----------------------------------

from app.users import models as user_models

from app.roles import models as role_models

from app.permissions import models as permission_models

from app.cameras import models as camera_models

from app.ai_models import models as ai_model_models

from app.mapping import models as mapping_models

from app.events import models as event_models









# ----------------------------------
# Seed
# ----------------------------------

from app.permissions.service import seed_permissions









# ----------------------------------
# Routers
# ----------------------------------

from app.auth.router import router as auth_router

from app.roles.router import router as roles_router

from app.users.router import router as users_router

from app.permissions.router import router as permissions_router

from app.cameras.router import router as cameras_router

from app.ai_models.router import router as ai_models_router

from app.mapping.router import router as mapping_router

from app.events.router import router as events_router

from app.dashboard.router import router as dashboard_router

from app.setup.router import router as setup_router










# ----------------------------------
# Background Service
# ----------------------------------

from app.cameras.monitor import camera_monitor










# ----------------------------------
# Paths
# ----------------------------------

BASE_DIR = (

    Path(__file__)

    .resolve()

    .parent

    .parent

)






# Already handled in config.py
# DO NOT add BASE_DIR here

STORAGE_DIR = Path(

    settings.STORAGE_PATH

)


MODEL_DIR = Path(

    settings.MODEL_PATH

)


EVIDENCE_DIR = Path(

    settings.EVIDENCE_PATH

)





FRONTEND_DIR = (

    BASE_DIR

    /

    "frontend_dist"

)










# ----------------------------------
# Create Folders
# ----------------------------------

STORAGE_DIR.mkdir(

    parents=True,

    exist_ok=True

)


MODEL_DIR.mkdir(

    parents=True,

    exist_ok=True

)


EVIDENCE_DIR.mkdir(

    parents=True,

    exist_ok=True

)










# ----------------------------------
# Seed Database
# ----------------------------------

db = SessionLocal()


try:


    seed_permissions(

        db

    )


finally:


    db.close()










# ----------------------------------
# Startup / Shutdown
# ----------------------------------

monitor_task = None









@asynccontextmanager
async def lifespan(

    app: FastAPI

):


    global monitor_task




    logger.info(

        "🚀 Backend Started"

    )



    logger.info(

        f"Environment: {settings.ENVIRONMENT}"

    )



    logger.info(

        f"Storage Path: {STORAGE_DIR}"

    )



    logger.info(

        f"Evidence Path: {EVIDENCE_DIR}"

    )







    monitor_task = asyncio.create_task(

        camera_monitor()

    )






    logger.info(

        "📡 Camera Monitor Running"

    )






    yield









    logger.info(

        "🛑 Backend shutting down"

    )





    if monitor_task:


        monitor_task.cancel()










# ----------------------------------
# FastAPI App
# ----------------------------------

app = FastAPI(

    title=settings.APP_NAME,

    description="Enterprise AI Vision Monitoring Backend",

    version="1.0.0",

    lifespan=lifespan

)










# ----------------------------------
# CORS
# ----------------------------------

app.add_middleware(

    CORSMiddleware,


    allow_origins=[

        "*"

    ],


    allow_credentials=True,


    allow_methods=[

        "*"

    ],


    allow_headers=[

        "*"

    ]

)










# ----------------------------------
# Register Routers
# ----------------------------------

routers = [

    auth_router,

    roles_router,

    users_router,

    permissions_router,

    cameras_router,

    ai_models_router,

    mapping_router,

    events_router,

    dashboard_router,

    setup_router

]





for router in routers:


    app.include_router(

        router

    )











# ----------------------------------
# Storage Static Files
#
# /storage/...
# ----------------------------------

app.mount(

    "/storage",


    StaticFiles(

        directory=str(STORAGE_DIR)

    ),


    name="storage"

)










# ----------------------------------
# Evidence Static Files
#
# /evidence/image.jpg
# ----------------------------------

app.mount(

    "/evidence",


    StaticFiles(

        directory=str(EVIDENCE_DIR)

    ),


    name="evidence"

)











# ----------------------------------
# AI Model Files
# ----------------------------------

app.mount(

    "/models-storage",


    StaticFiles(

        directory=str(MODEL_DIR)

    ),


    name="models-storage"

)










# ----------------------------------
# React Assets
# ----------------------------------

if FRONTEND_DIR.exists():


    app.mount(

        "/assets",


        StaticFiles(

            directory=FRONTEND_DIR / "assets"

        ),


        name="assets"

    )










# ----------------------------------
# Health Check
# ----------------------------------

@app.get("/api/health")
def health():


    return {

        "status": "running",

        "environment": settings.ENVIRONMENT

    }










# ----------------------------------
# DB Test
# ----------------------------------

@app.get("/db-test")
def test_database(

    db: Session = Depends(get_db)

):


    result = db.execute(

        text(

            "SELECT 1"

        )

    )



    return {

        "database": "connected",

        "result": result.scalar()

    }










# ----------------------------------
# React Entry
# ----------------------------------

@app.get("/")
def frontend():


    index_file = (

        FRONTEND_DIR

        /

        "index.html"

    )



    if index_file.exists():


        return FileResponse(

            index_file

        )



    return {

        "error": "frontend missing"

    }











# ----------------------------------
# React Router Support
# ----------------------------------

@app.get("/{full_path:path}")
def react_routes(

    full_path: str

):


    index_file = (

        FRONTEND_DIR

        /

        "index.html"

    )



    if index_file.exists():


        return FileResponse(

            index_file

        )



    return {

        "error": "frontend missing"

    }