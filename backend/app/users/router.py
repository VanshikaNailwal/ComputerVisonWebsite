from fastapi import (

    APIRouter,

    Depends

)



from sqlalchemy.orm import Session





from app.database import get_db





from app.users.schemas import (

    UserRegisterRequest,

    UserResponse

)





from app.users.service import (

    register_user,

    get_all_users,

    get_pending_users,

    approve_user,

    reject_user,

    delete_user

)





from app.auth.dependencies import (

    require_permission

)









router = APIRouter(

    prefix="/users",

    tags=["Users"]

)









# ----------------------------------
# Response Formatter
# ----------------------------------

def user_response(

    user

):


    return {


        "id":str(user.id),


        "employee_id":user.employee_id,


        "name":user.name,


        "email":user.email,


        "phone_number":user.phone_number,


        "department":user.department,


        "role":user.role.name,


        "status":user.status,


        "is_super_admin":user.is_super_admin


    }











# ----------------------------------
# Register User
# PUBLIC
# ----------------------------------

@router.post(

    "/register",

    response_model=UserResponse

)

def register_user_request(


    data:UserRegisterRequest,


    db:Session=Depends(get_db)

):



    user=register_user(

        db,

        data

    )




    return user_response(

        user

    )












# ----------------------------------
# Get All Users
# Permission: view_users
# ----------------------------------

@router.get(

    "",

    response_model=list[UserResponse]

)

def get_users(


    db:Session=Depends(get_db),


    current_user=Depends(

        require_permission(

            "view_users"

        )

    )

):




    users=get_all_users(

        db,


        current_user

    )






    return [


        user_response(user)


        for user in users


    ]












# ----------------------------------
# Pending Users
# Permission: view_users
# ----------------------------------

@router.get(

    "/pending",

    response_model=list[UserResponse]

)

def get_pending_requests(


    db:Session=Depends(get_db),


    current_user=Depends(

        require_permission(

            "view_users"

        )

    )

):




    users=get_pending_users(

        db,


        current_user

    )






    return [


        user_response(user)


        for user in users


    ]













# ----------------------------------
# Approve User
# Permission: manage_users
# ----------------------------------

@router.patch(

    "/{user_id}/approve",

    response_model=UserResponse

)

def approve_user_request(



    user_id:str,



    db:Session=Depends(get_db),



    current_user=Depends(

        require_permission(

            "manage_users"

        )

    )


):




    user=approve_user(

        db,


        user_id

    )





    return user_response(

        user

    )















# ----------------------------------
# Reject User
# Permission: manage_users
# ----------------------------------

@router.patch(

    "/{user_id}/reject",

    response_model=UserResponse

)

def reject_user_request(


    user_id:str,


    db:Session=Depends(get_db),


    current_user=Depends(

        require_permission(

            "manage_users"

        )

    )


):





    user=reject_user(

        db,


        user_id

    )






    return user_response(

        user

    )















# ----------------------------------
# Delete User
# Permission: manage_users
# ----------------------------------

@router.delete(

    "/{user_id}"

)

def delete_user_request(


    user_id:str,


    db:Session=Depends(get_db),


    current_user=Depends(

        require_permission(

            "manage_users"

        )

    )

):




    return delete_user(

        db,


        user_id,


        current_user

    )