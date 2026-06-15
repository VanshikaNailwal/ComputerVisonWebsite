from fastapi import HTTPException



from sqlalchemy.orm import Session



from app.users.models import User



from app.auth.security import (

    verify_password,

    hash_password,

    create_access_token

)





from app.email.email_service import send_reset_email





import secrets



from datetime import (

    datetime,

    timedelta

)













# ----------------------------------
# Login User
# ----------------------------------

def login_user(

    db: Session,

    email: str,

    password: str

):



    user = db.query(

        User

    ).filter(

        User.email == email

    ).first()







    if not user:



        raise HTTPException(

            status_code=401,

            detail="Invalid email or password"

        )









    if not verify_password(

        password,

        user.password

    ):



        raise HTTPException(

            status_code=401,

            detail="Invalid email or password"

        )









    if user.status != "ACTIVE":



        raise HTTPException(

            status_code=403,

            detail="Account pending admin approval"

        )









    # -----------------------------
    # Get Role Permissions
    # -----------------------------

    permissions = [

        permission.name

        for permission in user.role.permissions

    ]










    token = create_access_token(

        {


            "id": str(user.id),


            "role": user.role.name,


            "permissions": permissions


        }

    )












    return {



        "token": token,



        "user": {



            "id": str(user.id),



            "employee_id": user.employee_id,



            "name": user.name,



            "email": user.email,



            "phone_number": user.phone_number,



            "department": user.department,



            "role": user.role.name,



            "status": user.status,



            "is_super_admin": user.is_super_admin,



            "permissions": permissions



        }



    }

















# ----------------------------------
# Change Password
# ----------------------------------

def change_password(

    db: Session,

    user: User,

    old_password: str,

    new_password: str

):





    if not verify_password(

        old_password,

        user.password

    ):



        raise HTTPException(

            status_code=400,

            detail="Old password is incorrect"

        )










    if verify_password(

        new_password,

        user.password

    ):



        raise HTTPException(

            status_code=400,

            detail="New password cannot be same as old password"

        )










    user.password = hash_password(

        new_password

    )









    db.commit()










    return {

        "message":

        "Password changed successfully"

    }

















# ----------------------------------
# Forgot Password
# ----------------------------------

async def forgot_password(

    db: Session,

    email: str

):




    user = db.query(

        User

    ).filter(

        User.email == email

    ).first()











    if not user:



        raise HTTPException(

            status_code=404,

            detail="Email not registered"

        )












    token = secrets.token_urlsafe(

        32

    )












    user.reset_token = token







    user.reset_token_expiry = (

        datetime.utcnow()

        +

        timedelta(

            minutes=15

        )

    )












    db.commit()












    reset_link = (

        f"http://localhost:5173/reset-password?token={token}"

    )












    await send_reset_email(

        user.email,


        reset_link

    )












    return {


        "message":

        "Password reset link sent to your email"


    }

















# ----------------------------------
# Reset Password
# ----------------------------------

def reset_password(

    db: Session,

    token: str,

    new_password: str

):





    user = db.query(

        User

    ).filter(

        User.reset_token == token

    ).first()













    if not user:



        raise HTTPException(

            status_code=400,

            detail="Invalid reset link"

        )












    if user.reset_token_expiry < datetime.utcnow():



        raise HTTPException(

            status_code=400,

            detail="Reset link expired"

        )












    user.password = hash_password(

        new_password

    )











    user.reset_token = None



    user.reset_token_expiry = None












    db.commit()












    return {


        "message":

        "Password reset successfully"


    }