from pydantic import (

    BaseModel,

    EmailStr,

    field_validator

)



import re







# -----------------------------
# Login Request
# -----------------------------

class LoginRequest(BaseModel):


    email: EmailStr


    password: str







    @field_validator("email")
    def validate_email(cls,email):


        email=email.lower().strip()


        allowed_domains=[

            "hmel.com",

            "gmail.com"

        ]



        domain=email.split("@")[1]



        if domain not in allowed_domains:


            raise ValueError(

                "Only HMEL or Gmail accounts are allowed"

            )



        return email







    @field_validator("password")
    def validate_password(cls,password):


        if not password.strip():


            raise ValueError(

                "Password cannot be empty"

            )


        return password












# -----------------------------
# Login User Response
# -----------------------------

class LoginUser(BaseModel):


    id:str


    employee_id:str


    name:str


    email:str


    phone_number:str


    department:str


    role:str


    status:str


    is_super_admin:bool


    permissions:list[str]









# -----------------------------
# Login Response
# -----------------------------

class LoginResponse(BaseModel):


    token:str


    user:LoginUser












# -----------------------------
# Current User Response
# -----------------------------

class CurrentUserResponse(BaseModel):


    id:str


    employee_id:str


    name:str


    email:str


    phone_number:str


    department:str


    role:str


    status:str


    is_super_admin:bool


    permissions:list[str]













# -----------------------------
# Change Password
# -----------------------------

class ChangePasswordRequest(BaseModel):


    old_password:str


    new_password:str








    @field_validator("old_password")
    def validate_old_password(cls,password):


        if not password.strip():


            raise ValueError(

                "Old password cannot be empty"

            )


        return password







    @field_validator("new_password")
    def validate_new_password(cls,password):


        return validate_password_rules(

            password

        )














# -----------------------------
# Forgot Password
# -----------------------------

class ForgotPasswordRequest(BaseModel):


    email:EmailStr














# -----------------------------
# Reset Password
# -----------------------------

class ResetPasswordRequest(BaseModel):


    token:str


    new_password:str







    @field_validator("new_password")
    def validate_reset_password(cls,password):


        return validate_password_rules(

            password

        )














# -----------------------------
# Common Password Validator
# -----------------------------

def validate_password_rules(password):


    password=password.strip()




    if not password:


        raise ValueError(

            "Password cannot be empty"

        )





    if len(password)<8:


        raise ValueError(

            "Password must contain at least 8 characters"

        )






    if not re.search(

        r"[A-Z]",

        password

    ):


        raise ValueError(

            "Password must contain uppercase letter"

        )







    if not re.search(

        r"[a-z]",

        password

    ):


        raise ValueError(

            "Password must contain lowercase letter"

        )







    if not re.search(

        r"\d",

        password

    ):


        raise ValueError(

            "Password must contain number"

        )







    if not re.search(

        r"[!@#$%^&*]",

        password

    ):


        raise ValueError(

            "Password must contain special character"

        )







    return password