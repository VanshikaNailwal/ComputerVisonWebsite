from app.users.models import User

from app.roles.models import Role

from app.auth.security import hash_password

from app.core.config import settings








def create_default_admin(db):



    existing_admin = (

        db.query(User)

        .filter(

            User.is_super_admin == True

        )

        .first()

    )






    if existing_admin:


        print(

            "Super admin already exists"

        )


        return







    admin_role = (

        db.query(Role)

        .filter(

            Role.name=="ADMIN"

        )

        .first()

    )







    if not admin_role:


        admin_role = Role(

            name="ADMIN",

            description="System Administrator"

        )



        db.add(admin_role)


        db.commit()


        db.refresh(admin_role)









    admin = User(

        employee_id=settings.SUPER_ADMIN_EMPLOYEE_ID,


        name=settings.SUPER_ADMIN_NAME,


        email=settings.SUPER_ADMIN_EMAIL,


        password=hash_password(

            settings.SUPER_ADMIN_PASSWORD

        ),


        role_id=admin_role.id,


        status="ACTIVE",


        is_super_admin=True

    )








    db.add(admin)


    db.commit()





    print(

        "Super admin created successfully"

    )