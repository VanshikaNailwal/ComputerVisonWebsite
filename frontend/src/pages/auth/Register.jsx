import {

    useEffect,

    useState

} from "react";



import {

    Box,
    Button,
    TextField,
    Typography,
    MenuItem,
    Alert,
    InputAdornment

} from "@mui/material";



import {

    Visibility,
    VisibilityOff

} from "@mui/icons-material";



import axios from "axios";



import { useNavigate } from "react-router-dom";



import logo from "../../assets/HMEL_Logo.jpg";



import PasswordRules from "../../components/PasswordRules";









function Register(){



const navigate = useNavigate();



const [roles,setRoles] = useState([]);



const [error,setError] = useState("");



const [success,setSuccess] = useState("");



const [showPassword,setShowPassword] = useState(false);







const [form,setForm] = useState({



    name:"",


    employee_id:"",


    email:"",


    phone_number:"",


    department:"",


    role_id:"",


    password:"",


    confirmPassword:""



});











// -----------------------------
// Load Public Roles
// -----------------------------

useEffect(()=>{



axios.get(

    "http://localhost:8000/roles/public"

)


.then(res=>{



    setRoles(

        res.data

    );



})


.catch(()=>{



    setError(

        "Unable to load roles"

    );



});




},[]);











// -----------------------------
// Handle Input
// -----------------------------

const handleChange=(e)=>{



setError("");



setForm({


    ...form,


    [e.target.name]:e.target.value


});



};












// -----------------------------
// Validation
// -----------------------------

const validate=()=>{



if(!form.name.trim())

return "Full name required";



if(!form.employee_id.trim())

return "Employee ID required";



if(!form.email.trim())

return "Email required";



if(!form.phone_number.trim())

return "Phone number required";



if(form.phone_number.length!==10)

return "Phone number must be 10 digits";



if(!form.department)

return "Select department";



if(!form.role_id)

return "Select role";



if(!form.password)

return "Password required";



if(form.password!==form.confirmPassword)

return "Passwords do not match";




return "";



};












// -----------------------------
// Submit Request
// -----------------------------

const handleSubmit=async()=>{



const validationError=validate();




if(validationError){



    setError(

        validationError

    );



    return;


}









try{



await axios.post(

"http://localhost:8000/users/register",


{



employee_id:form.employee_id,



name:form.name,



email:form.email,



phone_number:form.phone_number,



department:form.department,



role_id:form.role_id,



password:form.password



}


);









setSuccess(

"Account request submitted. Waiting for admin approval."

);









setForm({


name:"",


employee_id:"",


email:"",


phone_number:"",


department:"",


role_id:"",


password:"",


confirmPassword:""



});





}



catch(err){



setError(

err.response?.data?.detail ||

"Registration failed"

);



}



};













return (

<Box

sx={{

minHeight:"100vh",

background:"#0d0f12",

color:"white",

display:"flex",

position:"relative",

overflow:"visible",

pb:8


}}

>










{/* LOGO */}


<Box

component="img"

src={logo}

onClick={()=>navigate("/login")}

sx={{


position:"absolute",


top:30,


left:40,


width:130,


background:"white",


borderRadius:2,


padding:1,


cursor:"pointer"



}}

/>









{/* LEFT */}


<Box

sx={{


flex:1,


height:"100vh",


position:"sticky",


top:0,


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

Request Access

</Typography>






<Typography

sx={{


mt:2,


fontSize:20,


color:"#9ca3af"



}}

>

HMEL Vision AI Monitoring Platform

</Typography>




</Box>













{/* FORM */}


<Box

sx={{


width:430,


mr:"7%",


pt:"120px",


pb:"80px",


display:"flex",


flexDirection:"column"



}}

>









<Typography

variant="h4"

fontWeight={800}

mb={3}

>

Employee Details

</Typography>









<TextField

placeholder="Full Name"

name="name"

value={form.name}

onChange={handleChange}

sx={fieldStyle}

/>







<TextField

placeholder="Employee ID"

name="employee_id"

value={form.employee_id}

onChange={handleChange}

sx={fieldStyle}

/>








<TextField

placeholder="Email"

name="email"

value={form.email}

onChange={handleChange}

sx={fieldStyle}

/>








<TextField

placeholder="Phone Number"

name="phone_number"

value={form.phone_number}

onChange={handleChange}

sx={fieldStyle}

/>









<TextField

select

name="department"

value={form.department}

onChange={handleChange}

SelectProps={{

displayEmpty:true

}}

sx={fieldStyle}

>


<MenuItem value="">

Department

</MenuItem>



<MenuItem value="IT">IT</MenuItem>


<MenuItem value="Operations">Operations</MenuItem>


<MenuItem value="Safety">Safety</MenuItem>


<MenuItem value="Maintenance">Maintenance</MenuItem>



</TextField>











<TextField

select

name="role_id"

value={form.role_id}

onChange={handleChange}

SelectProps={{

displayEmpty:true

}}

sx={fieldStyle}

>



<MenuItem value="">

Role

</MenuItem>






{


roles.map(role=>(


<MenuItem


key={role.id}


value={role.id}

>


{role.name}


</MenuItem>


))


}




</TextField>











<TextField

placeholder="Password"

name="password"

type={showPassword ? "text":"password"}

value={form.password}

onChange={handleChange}

InputProps={{


endAdornment:(



<InputAdornment position="end">



<Box

onClick={()=>setShowPassword(!showPassword)}

sx={{


cursor:"pointer",


color:"white"


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











<TextField

placeholder="Confirm Password"

name="confirmPassword"

type="password"

value={form.confirmPassword}

onChange={handleChange}

sx={fieldStyle}

/>









<PasswordRules

password={form.password}

/>









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











<Button

onClick={handleSubmit}

sx={{


height:52,


background:"#f97316",


color:"white",


fontWeight:800,


borderRadius:2,



"&:hover":{


background:"#ea580c"


}



}}

>


SUBMIT REQUEST


</Button>











<Typography

mt={3}

textAlign="center"

color="#94a3b8"

>


Already approved?



<span


onClick={()=>navigate("/login")}


style={{


color:"#f97316",


marginLeft:5,


cursor:"pointer"



}}

>


Login


</span>



</Typography>







</Box>



</Box>


);



}









const fieldStyle={



mb:2.5,


background:"#161b22",


borderRadius:2,




"& .MuiInputBase-root":{


height:54


},




input:{


color:"white"


},




"& fieldset":{


border:"1px solid #263244"


},




"&:hover fieldset":{


border:"1px solid #f97316"


},




"& .MuiSelect-select":{


color:"white"


},




"& svg":{


color:"white"


}



};









export default Register;