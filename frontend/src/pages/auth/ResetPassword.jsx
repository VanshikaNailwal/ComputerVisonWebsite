import { useState } from "react";



import {

    Box,
    Button,
    TextField,
    Typography,
    Alert,
    InputAdornment,
    IconButton

} from "@mui/material";



import {

    Visibility,
    VisibilityOff

} from "@mui/icons-material";



import {

    useNavigate,
    useSearchParams

} from "react-router-dom";



import api from "../../api/axios";



import PasswordRules from "../../components/PasswordRules";



import logo from "../../assets/HMEL_Logo.jpg";









function ResetPassword(){



const navigate = useNavigate();



const [searchParams] = useSearchParams();



const token = searchParams.get(

    "token"

);









const [password,setPassword] = useState("");



const [showPassword,setShowPassword] = useState(false);



const [error,setError] = useState("");



const [success,setSuccess] = useState("");



const [loading,setLoading] = useState(false);













// -----------------------------
// Reset Password API
// -----------------------------

const handleResetPassword = async()=>{





try{



setError("");

setSuccess("");

setLoading(true);









const response = await api.patch(

    "/auth/reset-password",

    {


        token:token,


        new_password:password


    }

);









setSuccess(

    response.data.message

);









setTimeout(()=>{


    navigate(

        "/login"

    );


},1500);








}



catch(error){





const message =


error.response?.data?.detail


||


"Password reset failed";









if(Array.isArray(message)){



    setError(

        message[0].msg

    );



}



else{


    setError(

        message

    );


}



}




finally{


setLoading(false);


}





};









return(



<Box

sx={{

    minHeight:"100vh",

    background:"#0f172a",

    display:"flex",

    alignItems:"center",

    justifyContent:"center",

    p:2

}}

>









<Box

sx={{

    width:420,

    background:"#111827",

    border:"1px solid #1f2937",

    borderRadius:3,

    p:4,

    color:"white"

}}

>








<Box

component="img"

src={logo}

sx={{

    width:90,

    display:"block",

    mx:"auto",

    mb:2,

    background:"white",

    borderRadius:1,

    p:.5

}}

/>









<Typography

variant="h5"

fontWeight={900}

textAlign="center"

>

Reset Password

</Typography>







<Typography

color="#94a3b8"

textAlign="center"

mt={1}

mb={3}

>

Create your new password

</Typography>










{

error &&


<Alert

severity="error"

sx={{mb:2}}

>

{error}

</Alert>


}










{

success &&


<Alert

severity="success"

sx={{mb:2}}

>

{success}

</Alert>


}












<TextField


fullWidth


label="New Password"


type={

showPassword

?

"text"

:

"password"

}


value={password}


onChange={(e)=>

setPassword(

    e.target.value

)

}


sx={inputStyle}


InputProps={{


endAdornment:(


<InputAdornment position="end">



<IconButton


onClick={()=>

setShowPassword(

!showPassword

)

}


>


{


showPassword

?

<VisibilityOff sx={{color:"#94a3b8"}}/>


:


<Visibility sx={{color:"#94a3b8"}}/>


}



</IconButton>



</InputAdornment>


)


}}


/>











<PasswordRules

password={password}

/>










<Button


fullWidth


disabled={loading}


onClick={handleResetPassword}


sx={{

    mt:3,

    background:"#f97316",

    color:"white",

    fontWeight:800,


    "&:hover":{

        background:"#ea580c"

    }

}}

>


{

loading

?

"Updating..."

:

"Update Password"

}


</Button>











<Button


fullWidth


onClick={()=>

navigate("/login")

}


sx={{

mt:2,

color:"#94a3b8"

}}

>


Back to Login


</Button>









</Box>



</Box>



);



}













const inputStyle={



"& label":{


color:"#94a3b8"


},






"& label.Mui-focused":{


color:"#f97316"


},






"& input":{


color:"white"


},






"& fieldset":{


borderColor:"#334155"


},






"&:hover fieldset":{


borderColor:"#f97316"


},






"& .MuiOutlinedInput-root.Mui-focused fieldset":{


borderColor:"#f97316"


}




};









export default ResetPassword;