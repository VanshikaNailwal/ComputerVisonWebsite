from fastapi import HTTPException


from sqlalchemy.orm import Session



from app.roles.models import Role


from app.permissions.models import Permission


from app.users.models import User











# ----------------------------------
# Create Role
# ----------------------------------

def create_role(

    db:Session,

    data

):




    existing = db.query(

        Role

    ).filter(

        Role.name == data.name.upper()

    ).first()







    if existing:


        raise HTTPException(

            status_code=400,

            detail="Role already exists"

        )









    role = Role(


        name=data.name.upper(),


        description=data.description


    )








    # attach permissions

    permissions = db.query(

        Permission

    ).filter(

        Permission.name.in_(

            data.permissions

        )

    ).all()








    role.permissions = permissions







    db.add(

        role

    )



    db.commit()



    db.refresh(

        role

    )







    return role















# ----------------------------------
# Get All Roles
# ----------------------------------

def get_all_roles(

    db:Session

):



    return db.query(

        Role

    ).all()

















# ----------------------------------
# Update Role
# ----------------------------------

def update_role(

    db:Session,

    role_id,

    data

):




    role = db.query(

        Role

    ).filter(

        Role.id == role_id

    ).first()









    if not role:


        raise HTTPException(

            status_code=404,

            detail="Role not found"

        )










    # protect main ADMIN role

    if role.name == "ADMIN":



        raise HTTPException(

            status_code=403,

            detail="ADMIN role cannot be modified"

        )









    role.name = data.name.upper()



    role.description = data.description










    permissions = db.query(

        Permission

    ).filter(

        Permission.name.in_(

            data.permissions

        )

    ).all()









    role.permissions = permissions










    db.commit()



    db.refresh(

        role

    )







    return role



















# ----------------------------------
# Delete Role
# ----------------------------------

def delete_role(

    db:Session,

    role_id

):




    role = db.query(

        Role

    ).filter(

        Role.id == role_id

    ).first()









    if not role:


        raise HTTPException(

            status_code=404,

            detail="Role not found"

        )












    # protect ADMIN

    if role.name == "ADMIN":



        raise HTTPException(

            status_code=403,

            detail="ADMIN role cannot be deleted"

        )










    # check assigned users

    user = db.query(

        User

    ).filter(

        User.role_id == role.id

    ).first()







    if user:



        raise HTTPException(

            status_code=400,

            detail="Cannot delete role assigned to users"

        )










    db.delete(

        role

    )



    db.commit()









    return {


        "message":"Role deleted successfully"


    }