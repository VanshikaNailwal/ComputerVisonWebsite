from pydantic import BaseModel, EmailStr






class SuperAdminCreate(BaseModel):


    employee_id:str


    name:str


    email:EmailStr


    phone_number:str


    department:str


    password:str