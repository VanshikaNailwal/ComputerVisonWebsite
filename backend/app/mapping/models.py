from sqlalchemy import (

    Column,

    Integer,

    ForeignKey

)



from sqlalchemy.dialects.postgresql import UUID



from sqlalchemy.orm import relationship



from app.database import Base










class CameraModelMapping(Base):


    __tablename__ = "camera_model_mapping"








    id = Column(

        Integer,

        primary_key=True,

        index=True

    )









    # ----------------------------------
    # Camera ID
    # ----------------------------------

    camera_id = Column(

        UUID(as_uuid=True),

        ForeignKey(

            "cameras.id",

            ondelete="CASCADE"

        ),

        nullable=False

    )









    # ----------------------------------
    # AI Model ID
    # ----------------------------------

    model_id = Column(

        Integer,

        ForeignKey(

            "ai_models.id",

            ondelete="CASCADE"

        ),

        nullable=False

    )









    # ----------------------------------
    # Camera Relationship
    # ----------------------------------

    camera = relationship(

        "Camera",

        back_populates="model_mappings"

    )










    # ----------------------------------
    # AI Model Relationship
    # ----------------------------------

    ai_model = relationship(

        "AIModel"

    )