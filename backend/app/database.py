from sqlalchemy import create_engine


from sqlalchemy.orm import (

    sessionmaker,

    declarative_base

)



from app.core.config import settings







# ----------------------------------
# Database Engine
# ----------------------------------

engine = create_engine(

    settings.DATABASE_URL,

    pool_pre_ping=True

)









# ----------------------------------
# Database Session
# ----------------------------------

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)










# ----------------------------------
# Base Model
# ----------------------------------

Base = declarative_base()











# ----------------------------------
# Dependency
# Provides DB session to FastAPI
# ----------------------------------

def get_db():



    db = SessionLocal()



    try:


        yield db



    finally:


        db.close()