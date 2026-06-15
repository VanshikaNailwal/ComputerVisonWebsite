from datetime import (

    datetime,

    timedelta,

    timezone

)



from jose import (

    jwt,

    JWTError

)



from passlib.context import CryptContext



from app.core.config import settings







# --------------------------------
# Password Hashing Configuration
# --------------------------------

pwd_context = CryptContext(

    schemes=["bcrypt"],

    deprecated="auto"

)










# --------------------------------
# Convert Password → Hash
# --------------------------------

def hash_password(

    password: str

):


    return pwd_context.hash(

        password

    )









# --------------------------------
# Verify Password
# --------------------------------

def verify_password(

    plain_password: str,


    hashed_password: str

):


    return pwd_context.verify(

        plain_password,


        hashed_password

    )










# --------------------------------
# Create JWT Access Token
# --------------------------------

def create_access_token(

    data: dict

):



    token_data = data.copy()





    expire_time = (

        datetime.now(

            timezone.utc

        )

        +

        timedelta(

            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES

        )

    )







    token_data.update(

        {

            "exp": expire_time,


            "type": "access"

        }

    )








    token = jwt.encode(

        token_data,


        settings.SECRET_KEY,


        algorithm=settings.ALGORITHM

    )







    return token











# --------------------------------
# Decode / Verify JWT Token
# --------------------------------

def verify_token(

    token: str

):



    try:



        payload = jwt.decode(

            token,


            settings.SECRET_KEY,


            algorithms=[

                settings.ALGORITHM

            ]

        )





        return payload






    except JWTError:



        return None