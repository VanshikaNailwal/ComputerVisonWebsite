import { useState } from "react";


import {

    Box,
    Button,
    TextField,
    Typography,
    Alert

} from "@mui/material";


import { useNavigate } from "react-router-dom";


import api from "../../api/axios";


import logo from "../../assets/HMEL_Logo.jpg";









function ForgotPassword(){


const navigate = useNavigate();



const [email,setEmail] = useState("");

const [error,setError] = useState("");

const [success,setSuccess] = useState("");

const [loading,setLoading] = useState(false);










const handleSubmit = async()=>{


try{


setError("");

setSuccess("");

setLoading(true);




const response = await api.post(

    "/auth/forgot-password",

    {

        email:email

    }

);





setSuccess(

    response.data.message

);





}

catch(error){



const msg =

error.response?.data?.detail

||

"Something went wrong";



setError(

Array.isArray(msg)

?

msg[0].msg

:

msg

);



}

finally{


setLoading(false);


}



};










return(


<Box

sx={{

minHeight:"100vh",

display:"flex",

alignItems:"center",

justifyContent:"center",

background:"#0f172a",

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

borderRadius:1

}}

/>





<Typography

variant="h5"

fontWeight={800}

textAlign="center"

mb={1}

>

Forgot Password

</Typography>






<Typography

color="#94a3b8"

textAlign="center"

mb={3}

>

Enter your registered email

</Typography>






{

error &&

<Alert severity="error" sx={{mb:2}}>

{error}

</Alert>

}





{

success &&

<Alert severity="success" sx={{mb:2}}>

{success}

</Alert>

}








<TextField

fullWidth

label="Email"

value={email}

onChange={(e)=>setEmail(e.target.value)}

sx={inputStyle}

/>









<Button

fullWidth

disabled={loading}

onClick={handleSubmit}

sx={{

mt:3,

background:"#f97316",

color:"white",

fontWeight:700

}}

>

{

loading

?

"Sending..."

:

"Send Reset Link"

}

</Button>









<Button

fullWidth

onClick={()=>navigate("/login")}

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


"& input":{

color:"white"

},


"& fieldset":{

borderColor:"#334155"

}

};




export default ForgotPassword;