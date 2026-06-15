from fastapi_mail import (

    FastMail,

    MessageSchema,

    ConnectionConfig

)










# ----------------------------------
# Gmail SMTP Configuration
# ----------------------------------

conf = ConnectionConfig(


    MAIL_USERNAME="vanshikanail@gmail.com",



    # Gmail 16 character app password
    # remove spaces

    MAIL_PASSWORD="abxd efgh ighj mnop",



    MAIL_FROM="vanshika@gmail.com",





    # Gmail SSL Port

    MAIL_PORT=587,



    MAIL_SERVER="smtp.gmail.com",





    # Port 465 uses SSL

    MAIL_STARTTLS=False,



    MAIL_SSL_TLS=True,






    USE_CREDENTIALS=True,



    VALIDATE_CERTS=True


)













# ----------------------------------
# Send Reset Password Email
# ----------------------------------

async def send_reset_email(

    email: str,

    reset_link: str

):



    message = MessageSchema(



        subject="HMEL Vision AI Password Reset",




        recipients=[

            email

        ],




        body=f"""


Hello,


You requested a password reset for your HMEL Vision AI account.


Click the link below to reset your password:


{reset_link}



This link expires in 15 minutes.



If you did not request this password reset,
you can safely ignore this email.



Regards,

HMEL Vision AI Team


""",





        subtype="plain"


    )









    fm = FastMail(

        conf

    )









    await fm.send_message(

        message

    )