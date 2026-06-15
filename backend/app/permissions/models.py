from sqlalchemy import (

    Column,

    String,

    DateTime,

    Table,

    ForeignKey

)



from sqlalchemy.dialects.postgresql import UUID



from sqlalchemy.orm import relationship



from datetime import datetime



import uuid




from app.database import Base







# ----------------------------------
# Role Permission Mapping Table
# ----------------------------------

role_permissions = Table(

    "role_permissions",

    Base.metadata,



    Column(

        "role_id",

        UUID(as_uuid=True),

        ForeignKey(

            "roles.id",

            ondelete="CASCADE"

        ),

        primary_key=True

    ),




    Column(

        "permission_id",

        UUID(as_uuid=True),

        ForeignKey(

            "permissions.id",

            ondelete="CASCADE"

        ),

        primary_key=True

    )

)









# ----------------------------------
# Permissions Table
# ----------------------------------

class Permission(Base):


    __tablename__ = "permissions"






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








    roles = relationship(

        "Role",

        secondary=role_permissions,

        back_populates="permissions"

    )