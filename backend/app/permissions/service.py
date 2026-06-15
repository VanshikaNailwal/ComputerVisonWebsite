from sqlalchemy.orm import Session



from app.permissions.models import Permission









DEFAULT_PERMISSIONS = [



    (

        "view_dashboard",

        "Access dashboard"

    ),



    (

        "view_users",

        "View users"

    ),



    (

        "manage_users",

        "Create update delete users"

    ),



    (

        "view_roles",

        "View roles"

    ),



    (

        "manage_roles",

        "Manage roles and permissions"

    ),



    (

        "view_cameras",

        "View cameras"

    ),



    (

        "manage_cameras",

        "Manage cameras"

    ),



    (

        "view_models",

        "View AI models"

    ),



    (

        "manage_models",

        "Manage AI models"

    ),



    (

        "manage_mapping",

        "Assign models to cameras"

    ),



    (

        "view_alerts",

        "View alerts"

    ),



    (

        "manage_alerts",

        "Manage alerts"

    )

]









def seed_permissions(

    db: Session

):



    for name,description in DEFAULT_PERMISSIONS:




        exists = db.query(

            Permission

        ).filter(

            Permission.name == name

        ).first()








        if not exists:



            permission = Permission(

                name=name,

                description=description

            )



            db.add(

                permission

            )






    db.commit()












def get_all_permissions(

    db: Session

):


    return db.query(

        Permission

    ).all()