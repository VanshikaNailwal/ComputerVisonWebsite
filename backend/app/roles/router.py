from fastapi import (

    APIRouter,

    Depends

)



from sqlalchemy.orm import Session





from app.database import get_db





from app.roles.schemas import (

    RoleCreate,

    RoleResponse

)





from app.roles.service import (

    create_role,

    get_all_roles,

    update_role,

    delete_role

)





from app.auth.dependencies import (

    require_permission

)









router = APIRouter(

    prefix="/roles",

    tags=["Roles"]

)












# ----------------------------------
# Role Response Converter
# ----------------------------------

def role_response(

    role

):


    return {


        "id":str(role.id),


        "name":role.name,


        "description":role.description,


        "permissions":[


            permission.name


            for permission in role.permissions


        ]


    }














# ----------------------------------
# PUBLIC ROLES
# Used in Register Page
# No Login Required
# ----------------------------------

@router.get(

    "/public"

)

def public_roles(

    db:Session=Depends(get_db)

):



    roles=get_all_roles(

        db

    )







    return [


        {


            "id":str(role.id),


            "name":role.name


        }


        for role in roles


        if role.name!="ADMIN"


    ]

















# ----------------------------------
# Create Role
# Permission : manage_roles
# ----------------------------------

@router.post(

    "",

    response_model=RoleResponse

)

def add_role(


    data:RoleCreate,


    db:Session=Depends(get_db),


    current_user=Depends(

        require_permission(

            "manage_roles"

        )

    )


):




    role=create_role(

        db,

        data

    )








    return role_response(

        role

    )















# ----------------------------------
# Get All Roles
# Permission : view_roles
# ----------------------------------

@router.get(

    "",

    response_model=list[RoleResponse]

)

def roles(


    db:Session=Depends(get_db),


    current_user=Depends(

        require_permission(

            "view_roles"

        )

    )


):




    roles=get_all_roles(

        db

    )








    return [


        role_response(

            role

        )


        for role in roles


    ]

















# ----------------------------------
# Update Role
# Permission : manage_roles
# ----------------------------------

@router.patch(

    "/{role_id}",

    response_model=RoleResponse

)

def update(


    role_id:str,


    data:RoleCreate,


    db:Session=Depends(get_db),


    current_user=Depends(

        require_permission(

            "manage_roles"

        )

    )


):





    role=update_role(

        db,

        role_id,

        data

    )








    return role_response(

        role

    )


















# ----------------------------------
# Delete Role
# Permission : manage_roles
# ----------------------------------

@router.delete(

    "/{role_id}"

)

def delete(


    role_id:str,


    db:Session=Depends(get_db),


    current_user=Depends(

        require_permission(

            "manage_roles"

        )

    )


):




    return delete_role(

        db,

        role_id

    )