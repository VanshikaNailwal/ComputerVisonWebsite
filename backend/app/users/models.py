from sqlalchemy import (

    Column,

    String,

    DateTime,

    ForeignKey,

    Boolean

)



from sqlalchemy.dialects.postgresql import UUID



from sqlalchemy.orm import relationship



from datetime import datetime



import uuid





from app.database import Base











class User(Base):


    __tablename__ = "users"









    id = Column(

        UUID(as_uuid=True),

        primary_key=True,

        default=uuid.uuid4

    )









    employee_id = Column(

        String,

        unique=True,

        nullable=False

    )








    name = Column(

        String,

        nullable=False

    )








    email = Column(

        String,

        unique=True,

        nullable=False

    )









    phone_number = Column(

        String,

        nullable=False

    )









    department = Column(

        String,

        nullable=False

    )












    password = Column(

        String,

        nullable=False

    )











    reset_token = Column(

        String,

        nullable=True

    )









    reset_token_expiry = Column(

        DateTime,

        nullable=True

    )













    role_id = Column(

        UUID(as_uuid=True),

        ForeignKey("roles.id"),

        nullable=False

    )








    role = relationship(

        "Role"

    )













    status = Column(

        String,

        default="PENDING"

    )













    # ----------------------------------
    # Super Admin Protection
    # ----------------------------------

    is_super_admin = Column(

        Boolean,

        default=False

    )













    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )