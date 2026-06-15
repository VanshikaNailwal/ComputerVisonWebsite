from fastapi import (

    Depends,

    HTTPException,

    status

)



from fastapi.security import (

    HTTPBearer,

    HTTPAuthorizationCredentials

)



from jose import (

    JWTError,

    jwt

)



from sqlalchemy.orm import Session





from app.core import settings



from app.database import get_db



from app.users.models import User












# --------------------------------
# Bearer Token
# --------------------------------

security = HTTPBearer()












# --------------------------------
# Get Logged In User
# --------------------------------

def get_current_user(


    credentials: HTTPAuthorizationCredentials = Depends(security),


    db: Session = Depends(get_db)

):




    token = credentials.credentials







    try:



        payload = jwt.decode(

            token,

            settings.SECRET_KEY,

            algorithms=[settings.ALGORITHM]

        )








        if payload.get("type") != "access":



            raise HTTPException(

                status_code=status.HTTP_401_UNAUTHORIZED,

                detail="Invalid token type"

            )








        user_id = payload.get("id")








        if not user_id:



            raise HTTPException(

                status_code=status.HTTP_401_UNAUTHORIZED,

                detail="Invalid token"

            )









    except JWTError:



        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Token expired or invalid"

        )













    user = db.query(

        User

    ).filter(

        User.id == user_id

    ).first()









    if not user:



        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="User not found"

        )









    if user.status != "ACTIVE":



        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Account disabled"

        )








    return user

















# --------------------------------
# Permission Based Security
# --------------------------------

def require_permission(

    permission_name:str

):



    def checker(

        current_user:User = Depends(get_current_user)

    ):





        # SUPER ADMIN ALWAYS ALLOWED

        if current_user.is_super_admin:



            return current_user









        user_permissions = [


            permission.name


            for permission in current_user.role.permissions


        ]









        if permission_name not in user_permissions:



            raise HTTPException(

                status_code=status.HTTP_403_FORBIDDEN,

                detail="Permission denied"

            )










        return current_user







    return checker















# --------------------------------
# Old Admin Checker
# kept for compatibility
# --------------------------------

def require_admin(

    current_user:User = Depends(get_current_user)

):



    if current_user.is_super_admin:



        return current_user









    if current_user.role.name != "ADMIN":



        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Admin access required"

        )








    return current_user