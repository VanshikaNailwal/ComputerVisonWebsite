from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.database import Base


class AIModel(Base):

    __tablename__ = "ai_models"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    # ----------------------------------
    # Model Details
    # ----------------------------------

    usecase = Column(
        String,
        nullable=True
    )

    version = Column(
        String,
        nullable=True
    )

    # ----------------------------------
    # YOLO Model File (.pt)
    # ----------------------------------

    filename = Column(
        String,
        nullable=False
    )

    file_path = Column(
        String,
        nullable=False
    )

    # ----------------------------------
    # Validation Status
    # CHECKING / READY / FAILED
    # ----------------------------------

    status = Column(
        String,
        default="CHECKING"
    )