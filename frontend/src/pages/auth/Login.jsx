import { useState } from "react";


import {

    Box,

    Button,

    TextField,

    Typography,

    InputAdornment,

    Alert

} from "@mui/material";



import {

    Visibility,

    VisibilityOff,

    Email,

    Lock

} from "@mui/icons-material";



import { useNavigate } from "react-router-dom";



import { useAuth } from "../../context/AuthContext";



import logo from "../../assets/HMEL_Logo.jpg";










function Login(){



const navigate = useNavigate();



const { login } = useAuth();





const [showPassword,setShowPassword] = useState(false);



const [error,setError] = useState("");




const [form,setForm] = useState({


    email:"",


    password:""


});










const handleChange = (e)=>{


    setError("");



    setForm({


        ...form,


        [e.target.name]:e.target.value


    });


};











const validate = ()=>{



    if(!form.email.trim()){


        return "Email is required";


    }






    const emailRegex=/^[^\s@]+@[^\s@]+\.[^\s@]+$/;





    if(!emailRegex.test(form.email)){



        return "Enter a valid email address";


    }







    if(!form.password){


        return "Password is required";


    }





    return "";


};











const handleLogin = async ()=>{



    const validationError = validate();





    if(validationError){


        setError(validationError);


        return;


    }






    try{



        await login(


            form.email,


            form.password


        );





        navigate("/");


    }



    catch(error){



        const message =


            error.response?.data?.detail


            ||


            "Login failed";





        if(Array.isArray(message)){



            setError(

                message[0].msg

            );


        }


        else{


            setError(message);


        }


    }


};












return (


<Box

sx={{


height:"100vh",


width:"100%",


background:"#0d0f12",


color:"white",


position:"relative",


overflow:"hidden",


display:"flex"


}}

>









<Box

component="img"

src={logo}

sx={{


position:"absolute",


top:30,


left:40,


width:130,


background:"white",


borderRadius:2,


padding:1


}}

/>










<Box

sx={{


flex:1,


display:"flex",


justifyContent:"center",


alignItems:"center",


flexDirection:"column"


}}

>



<Typography

variant="h2"

fontWeight={900}

>

HMEL Vision AI

</Typography>







<Typography

variant="h5"

sx={{


mt:2,


color:"#9ca3af"


}}

>

AI Powered Monitoring Platform

</Typography>









<Typography

sx={{


width:"520px",


mt:3,


lineHeight:1.8,


color:"#8b98aa",


fontSize:"18px",


textAlign:"center"


}}

>


Real-time camera analytics, model monitoring,
and intelligent alert management.


</Typography>



</Box>












<Box

sx={{


width:"420px",


marginRight:"5%",


display:"flex",


justifyContent:"center",


flexDirection:"column"


}}

>








<Typography

variant="h4"

fontWeight={800}

>

Welcome Back

</Typography>







<Typography

sx={{


color:"#9ca3af",


mb:5


}}

>

Login to continue monitoring

</Typography>












<TextField


placeholder="Email"


name="email"


value={form.email}


onChange={handleChange}


InputProps={{


startAdornment:(


<InputAdornment position="start">


<Email sx={{color:"#f97316"}} />


</InputAdornment>


)


}}


sx={fieldStyle}


/>









<TextField


placeholder="Password"


name="password"


value={form.password}


type={showPassword ? "text":"password"}


onChange={handleChange}



InputProps={{


startAdornment:(


<InputAdornment position="start">


<Lock sx={{color:"#f97316"}} />


</InputAdornment>


),



endAdornment:(


<InputAdornment position="end">


<Box


onClick={()=>setShowPassword(!showPassword)}


sx={{

cursor:"pointer",

color:"#f97316"

}}


>


{


showPassword


?


<VisibilityOff/>


:


<Visibility/>


}


</Box>


</InputAdornment>


)


}}


sx={fieldStyle}


/>











<Typography


onClick={()=>navigate("/forgot-password")}


sx={{


textAlign:"right",


mt:-1,


mb:2,


color:"#f97316",


cursor:"pointer"


}}

>

Forgot Password?


</Typography>









{

error &&


<Alert severity="error" sx={{mb:2}}>


{error}


</Alert>

}











<Button


onClick={handleLogin}


sx={{


height:52,


mt:2,


background:"#f97316",


color:"white",


fontWeight:800,


borderRadius:2,



"&:hover":{


background:"#ea580c"


}


}}

>

LOGIN

</Button>











<Typography

mt={3}

textAlign="center"

color="#9ca3af"

>

Need Access?



<span


onClick={()=>navigate("/register")}


style={{


color:"#f97316",


cursor:"pointer",


marginLeft:5


}}

>

Request Account

</span>



</Typography>







</Box>




</Box>


);


}









const fieldStyle={


mb:3,


background:"#161b22",


borderRadius:2,



input:{


color:"white"


},



"& input::placeholder":{


color:"#94a3b8",


opacity:1


},



"& .MuiSvgIcon-root":{


color:"#f97316"


},



"& fieldset":{


border:"none"


}


};






export default Login;