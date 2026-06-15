from pydantic import (

    BaseModel,

    EmailStr,

    field_validator

)


import re







# ----------------------------
# Register Request
# ----------------------------

class UserRegisterRequest(BaseModel):


    employee_id: str


    name: str


    email: EmailStr


    phone_number: str


    department: str


    role_id: str


    password: str







    @field_validator("email")
    def validate_email(cls,email):


        email=email.lower().strip()



        allowed=[

            "hmel.com",

            "gmail.com"

        ]



        domain=email.split("@")[1]



        if domain not in allowed:


            raise ValueError(

                "Only HMEL or Gmail emails allowed"

            )



        return email









    @field_validator("password")
    def validate_password(cls,password):


        if len(password)<8:


            raise ValueError(

                "Password must contain at least 8 characters"

            )





        if not re.search(

            r"[A-Z]",

            password

        ):


            raise ValueError(

                "Password needs uppercase letter"

            )






        if not re.search(

            r"[a-z]",

            password

        ):


            raise ValueError(

                "Password needs lowercase letter"

            )






        if not re.search(

            r"\d",

            password

        ):


            raise ValueError(

                "Password needs number"

            )






        if not re.search(

            r"[!@#$%^&*]",

            password

        ):


            raise ValueError(

                "Password needs special character"

            )





        return password












# ----------------------------
# User Response
# ----------------------------

class UserResponse(BaseModel):


    id: str


    employee_id: str


    name: str


    email: str


    phone_number: str


    department: str


    role: str


    status: str