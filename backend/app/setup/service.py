from fastapi import HTTPException


from sqlalchemy.orm import Session



from app.users.models import User


from app.roles.models import Role


from app.auth.security import hash_password







# ----------------------------------
# Check setup status
# ----------------------------------

def is_setup_required(

    db: Session

):


    admin = (

        db.query(User)

        .filter(

            User.is_super_admin == True

        )

        .first()

    )



    return admin is None










# ----------------------------------
# Create first Super Admin
# ----------------------------------

def create_super_admin(

    db: Session,

    data

):



    # ----------------------------------
    # Allow only first setup
    # ----------------------------------

    if not is_setup_required(

        db

    ):



        raise HTTPException(

            status_code=400,

            detail="Setup already completed"

        )









    # ----------------------------------
    # Get ADMIN role
    #
    # Fresh install:
    # role table is empty
    # so create it automatically
    # ----------------------------------

    role = (

        db.query(Role)

        .filter(

            Role.name == "ADMIN"

        )

        .first()

    )









    if not role:



        role = Role(

            name="ADMIN",

            description="System Administrator"

        )




        db.add(

            role

        )



        db.commit()



        db.refresh(

            role

        )










    # ----------------------------------
    # Create Super Admin user
    # ----------------------------------

    user = User(


        employee_id=data.employee_id,


        name=data.name,


        email=data.email,


        phone_number=data.phone_number,


        department=data.department,


        password=hash_password(

            data.password

        ),


        role_id=role.id,


        status="ACTIVE",


        is_super_admin=True


    )










    db.add(

        user

    )



    db.commit()



    db.refresh(

        user

    )









    return user