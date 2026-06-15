from fastapi import HTTPException


from sqlalchemy.orm import Session


from app.users.models import User


from app.roles.models import Role


from app.auth.security import hash_password







# ==================================================
# Register New User Request
# ==================================================

def register_user(

    db: Session,

    data

):



    # -----------------------------
    # Check duplicate email
    # -----------------------------

    existing_email = (

        db.query(

            User

        )

        .filter(

            User.email == data.email

        )

        .first()

    )






    if existing_email:


        raise HTTPException(

            status_code=400,

            detail="Email already exists"

        )









    # -----------------------------
    # Check duplicate Employee ID
    # -----------------------------

    existing_employee = (

        db.query(

            User

        )

        .filter(

            User.employee_id == data.employee_id

        )

        .first()

    )







    if existing_employee:


        raise HTTPException(

            status_code=400,

            detail="Employee ID already exists"

        )









    # -----------------------------
    # Check Role Exists
    # -----------------------------

    role = (

        db.query(

            Role

        )

        .filter(

            Role.id == data.role_id

        )

        .first()

    )







    if not role:


        raise HTTPException(

            status_code=404,

            detail="Selected role does not exist"

        )









    # -----------------------------
    # Prevent public admin request
    # -----------------------------

    if role.name.upper() == "ADMIN":


        raise HTTPException(

            status_code=403,

            detail="Admin account cannot be requested"

        )









    user = User(

        employee_id=data.employee_id,


        name=data.name,


        email=data.email,


        phone_number=data.phone_number,


        department=data.department,


        role_id=role.id,


        password=hash_password(

            data.password

        ),


        status="PENDING",


        is_super_admin=False

    )









    db.add(

        user

    )


    db.commit()


    db.refresh(

        user

    )








    return user

















# ==================================================
# Get All Users
#
# Super Admin:
# sees everyone
#
# Normal Admin:
# cannot see super admin
# ==================================================

def get_all_users(

    db: Session,

    current_user=None

):



    query = db.query(

        User

    )







    if (

        current_user

        and

        not current_user.is_super_admin

    ):


        query = query.filter(

            User.is_super_admin == False

        )









    return query.all()

















# ==================================================
# Get Pending Users
# ==================================================

def get_pending_users(

    db: Session,

    current_user=None

):



    query = db.query(

        User

    ).filter(

        User.status == "PENDING"

    )








    if (

        current_user

        and

        not current_user.is_super_admin

    ):


        query = query.filter(

            User.is_super_admin == False

        )








    return query.all()

















# ==================================================
# Approve User
# ==================================================

def approve_user(

    db: Session,

    user_id

):



    user = (

        db.query(

            User

        )

        .filter(

            User.id == user_id

        )

        .first()

    )








    if not user:


        raise HTTPException(

            status_code=404,

            detail="User not found"

        )









    if user.status == "ACTIVE":


        raise HTTPException(

            status_code=400,

            detail="User already active"

        )









    user.status = "ACTIVE"








    db.commit()


    db.refresh(

        user

    )









    return user

















# ==================================================
# Reject User
# ==================================================

def reject_user(

    db: Session,

    user_id

):



    user = (

        db.query(

            User

        )

        .filter(

            User.id == user_id

        )

        .first()

    )








    if not user:


        raise HTTPException(

            status_code=404,

            detail="User not found"

        )









    if user.is_super_admin:


        raise HTTPException(

            status_code=403,

            detail="Super admin cannot be rejected"

        )










    user.status = "REJECTED"








    db.commit()


    db.refresh(

        user

    )









    return user

















# ==================================================
# Delete User
# ==================================================

def delete_user(

    db: Session,

    user_id,

    current_user=None

):



    user = (

        db.query(

            User

        )

        .filter(

            User.id == user_id

        )

        .first()

    )








    if not user:


        raise HTTPException(

            status_code=404,

            detail="User not found"

        )









    # -----------------------------
    # Super Admin Protection
    # -----------------------------

    if user.is_super_admin:


        raise HTTPException(

            status_code=403,

            detail="Super admin cannot be deleted"

        )









    db.delete(

        user

    )


    db.commit()









    return {

        "message":"User deleted successfully"

    }