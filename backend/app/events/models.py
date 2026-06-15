import uuid


from sqlalchemy import (

    Column,

    String,

    Float,

    DateTime,

    ForeignKey

)


from sqlalchemy.sql import func


from sqlalchemy.dialects.postgresql import UUID


from sqlalchemy.orm import relationship



from app.database import Base







class Event(Base):


    __tablename__ = "events"








    # -------------------------
    # Event ID
    # -------------------------

    id = Column(

        UUID(as_uuid=True),

        primary_key=True,

        default=uuid.uuid4,

        index=True

    )









    # -------------------------
    # Camera
    # -------------------------

    camera_id = Column(

        UUID(as_uuid=True),

        ForeignKey(

            "cameras.id"

        ),

        nullable=False

    )









    # -------------------------
    # AI Model
    # -------------------------

    model_id = Column(

        ForeignKey(

            "ai_models.id"

        ),

        nullable=False

    )










    # -------------------------
    # Detection Details
    # -------------------------

    event_type = Column(

        String,

        nullable=False

    )




    confidence = Column(

        Float,

        nullable=False

    )









    # -------------------------
    # Evidence Snapshot
    # -------------------------

    image_path = Column(

        String,

        nullable=True

    )









    # -------------------------
    # Alert Status
    # ACTIVE
    # RESOLVED
    # FALSE ALARM
    # -------------------------

    status = Column(

        String,

        default="ACTIVE",

        nullable=False

    )










    # -------------------------
    # Admin Resolution Details
    # -------------------------

    resolution_note = Column(

        String,

        nullable=True

    )




    resolved_by = Column(

        String,

        nullable=True

    )




    resolved_at = Column(

        DateTime(timezone=True),

        nullable=True

    )









    # -------------------------
    # Created Time
    # -------------------------

    created_at = Column(

        DateTime(timezone=True),

        server_default=func.now()

    )











    # -------------------------
    # Relationships
    # -------------------------

    camera = relationship(

        "Camera"

    )




    ai_model = relationship(

        "AIModel"

    )