import uuid


from sqlalchemy import (

    Column,

    String,

    ForeignKey

)



from sqlalchemy.dialects.postgresql import UUID



from sqlalchemy.orm import relationship



from app.database import Base










class Camera(Base):


    __tablename__ = "cameras"







    id = Column(

        UUID(as_uuid=True),

        primary_key=True,

        default=uuid.uuid4,

        index=True

    )









    name = Column(

        String,

        nullable=False

    )









    ip_address = Column(

        String,

        unique=True,

        nullable=False

    )









    location = Column(

        String,

        nullable=False

    )









    rtsp_url = Column(

        String,

        unique=True,

        nullable=False

    )









    # ----------------------------------
    # Camera enabled / disabled by admin
    # ACTIVE / INACTIVE
    # ----------------------------------

    status = Column(

        String,

        default="ACTIVE"

    )









    # ----------------------------------
    # Actual RTSP Connection Status
    #
    # CHECKING  🟡
    # ONLINE    🟢
    # OFFLINE   🔴
    # ----------------------------------

    connection_status = Column(

        String,

        nullable=False,

        default="CHECKING"

    )









    # ----------------------------------
    # Camera <-> AI Model Mapping
    #
    # One camera -> many models
    # One model  -> many cameras
    # ----------------------------------

    model_mappings = relationship(

        "CameraModelMapping",

        back_populates="camera",

        cascade="all, delete"

    )











    # ----------------------------------
    # Created By User
    # ----------------------------------

    created_by = Column(

        UUID(as_uuid=True),

        ForeignKey(

            "users.id"

        )

    )
