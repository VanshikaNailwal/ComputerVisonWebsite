from sqlalchemy import (

    Column,

    String,

    DateTime

)



from sqlalchemy.dialects.postgresql import UUID



from sqlalchemy.orm import relationship



from datetime import datetime



import uuid




from app.database import Base



from app.permissions.models import role_permissions









class Role(Base):


    __tablename__ = "roles"







    id = Column(

        UUID(as_uuid=True),

        primary_key=True,

        default=uuid.uuid4

    )








    name = Column(

        String,

        unique=True,

        nullable=False

    )









    description = Column(

        String,

        nullable=True

    )










    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )










    permissions = relationship(

        "Permission",

        secondary=role_permissions,

        back_populates="roles"

    )