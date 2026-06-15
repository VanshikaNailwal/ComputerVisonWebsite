from fastapi import (

    APIRouter,

    Depends

)



from sqlalchemy.orm import Session







from app.database import get_db







from app.users.models import User







from app.auth.dependencies import get_current_user







from app.auth.schemas import (

    LoginRequest,

    LoginResponse,

    CurrentUserResponse,

    ChangePasswordRequest,

    ForgotPasswordRequest,

    ResetPasswordRequest

)









from app.auth.service import (

    login_user,

    change_password,

    forgot_password,

    reset_password

)












router = APIRouter(

    prefix="/auth",

    tags=["Authentication"]

)













# ----------------------------------
# Login API
# ----------------------------------

@router.post(

    "/login",

    response_model=LoginResponse

)

def login(


    data: LoginRequest,


    db: Session = Depends(get_db)

):



    return login_user(

        db,


        data.email,


        data.password

    )















# ----------------------------------
# Current Logged User
# ----------------------------------

@router.get(

    "/me",

    response_model=CurrentUserResponse

)

def get_me(


    current_user: User = Depends(

        get_current_user

    )

):



    permissions = [

        permission.name

        for permission in current_user.role.permissions

    ]









    return {



        "id": str(current_user.id),



        "employee_id": current_user.employee_id,



        "name": current_user.name,



        "email": current_user.email,



        "phone_number": current_user.phone_number,



        "department": current_user.department,



        "role": current_user.role.name,



        "status": current_user.status,



        "is_super_admin": current_user.is_super_admin,



        "permissions": permissions



    }

















# ----------------------------------
# Change Password
# ----------------------------------

@router.patch(

    "/change-password"

)

def update_password(


    data: ChangePasswordRequest,


    db: Session = Depends(

        get_db

    ),


    current_user: User = Depends(

        get_current_user

    )

):



    return change_password(

        db,


        current_user,


        data.old_password,


        data.new_password

    )















# ----------------------------------
# Forgot Password
# ----------------------------------

@router.post(

    "/forgot-password"

)

async def forgot(


    data: ForgotPasswordRequest,


    db: Session = Depends(

        get_db

    )

):



    return await forgot_password(

        db,


        data.email

    )

















# ----------------------------------
# Reset Password
# ----------------------------------

@router.patch(

    "/reset-password"

)

def reset(


    data: ResetPasswordRequest,


    db: Session = Depends(

        get_db

    )

):



    return reset_password(

        db,


        data.token,


        data.new_password

    )