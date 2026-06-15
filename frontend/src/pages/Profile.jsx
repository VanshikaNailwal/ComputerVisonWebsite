import { useState } from "react";


import {

    Box,
    Typography,
    Button,
    Card,
    CardContent,
    Divider,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    Alert,
    Chip

} from "@mui/material";



import {

    Logout,
    Lock,
    AccountCircle,
    Security

} from "@mui/icons-material";



import { useNavigate } from "react-router-dom";


import { useAuth } from "../context/AuthContext";


import api from "../api/axios";


import PasswordRules from "../components/PasswordRules";









function Profile(){


const navigate = useNavigate();


const { user, logout } = useAuth();




const [open,setOpen] = useState(false);



const [password,setPassword] = useState({

old_password:"",

new_password:""

});



const [error,setError] = useState("");

const [success,setSuccess] = useState("");










const handleLogout=()=>{


logout();


navigate("/login");


};









const handleChangePassword=async()=>{


try{


setError("");

setSuccess("");





const response = await api.patch(

"/auth/change-password",

password

);






setSuccess(

response.data.message

);






setPassword({

old_password:"",

new_password:""

});







setTimeout(()=>{


setOpen(false);


setSuccess("");


},1500);



}


catch(error){



const message =

error.response?.data?.detail ||

"Password change failed";




if(Array.isArray(message)){


setError(message[0].msg);


}

else{


setError(message);


}



}


};









return (

<Box

sx={{

minHeight:"100vh",

background:"#0f172a",

color:"white",

p:3

}}

>









{/* HEADER */}


<Typography

variant="h4"

fontWeight={900}

>

Profile

</Typography>






<Typography

color="#94a3b8"

mb={4}

>

Manage your account and permissions

</Typography>











<Card

sx={{

maxWidth:800,

background:"#111827",

color:"white",

borderRadius:3,

border:"1px solid #1f2937"

}}

>


<CardContent sx={{p:4}}>









{/* USER */}


<Box

display="flex"

alignItems="center"

gap={2}

mb={3}

>


<AccountCircle

sx={{

fontSize:70,

color:"#f97316"

}}

/>






<Box>


<Typography

variant="h5"

fontWeight={800}

>

{user?.name}

</Typography>






<Typography color="#94a3b8">

{user?.email}

</Typography>



</Box>


</Box>









<Divider

sx={{

my:3,

borderColor:"#334155"

}}

/>









<Typography

variant="h6"

fontWeight={800}

mb={2}

>

Account Information

</Typography>








<Info

label="Employee ID"

value={user?.employee_id}

/>




<Info

label="Department"

value={user?.department}

/>




<Info

label="Role"

value={user?.role}

/>










{/* STATUS */}


<Box

display="flex"

alignItems="center"

gap={2}

mt={2}

>


<Typography

color="#94a3b8"

width={130}

>

Status

</Typography>





<Chip

label={user?.status}

sx={{

background:"#16a34a",

color:"white",

fontWeight:700

}}

/>


</Box>









{/* SUPER ADMIN */}


{

user?.is_super_admin &&


<Box mt={3}>


<Chip


icon={<Security/>}


label="SUPER ADMIN"


sx={{


background:"#f97316",


color:"white",


fontWeight:900,


"& svg":{

color:"white"

}


}}


/>


</Box>


}











{/* PERMISSIONS */}



<Box mt={4}>


<Typography

fontWeight={800}

mb={2}

>

Permissions

</Typography>






{


user?.permissions?.length > 0

?

user.permissions.map(permission=>(



<Chip


key={permission}


label={permission}


sx={{


m:.5,


background:"#334155",


color:"white"


}}


/>



))


:


<Typography color="#94a3b8">

No permissions assigned

</Typography>


}



</Box>









{/* ACTION BUTTONS */}


<Box

mt={5}

display="flex"

gap={2}

>


<Button

startIcon={<Lock/>}

onClick={()=>setOpen(true)}

sx={{

background:"#f97316",

color:"white",

fontWeight:700

}}

>

Change Password

</Button>








<Button

variant="outlined"

startIcon={<Logout/>}

onClick={handleLogout}

sx={{

borderColor:"#ef4444",

color:"#ef4444"

}}

>

Logout

</Button>



</Box>






</CardContent>


</Card>












{/* CHANGE PASSWORD POPUP */}


<Dialog

open={open}

onClose={()=>setOpen(false)}

fullWidth

PaperProps={{

sx:{

background:"#111827",

color:"white",

borderRadius:3

}

}}

>






<DialogTitle fontWeight={800}>

Change Password

</DialogTitle>







<DialogContent>



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

label="Old Password"

type="password"

fullWidth

margin="normal"

value={password.old_password}

onChange={(e)=>

setPassword({

...password,

old_password:e.target.value

})

}

sx={fieldStyle}

/>









<TextField

label="New Password"

type="password"

fullWidth

margin="normal"

value={password.new_password}

onChange={(e)=>

setPassword({

...password,

new_password:e.target.value

})

}

sx={fieldStyle}

/>







<PasswordRules

password={password.new_password}

/>




</DialogContent>







<DialogActions>


<Button

onClick={()=>setOpen(false)}

>

Cancel

</Button>





<Button

onClick={handleChangePassword}

sx={{

background:"#f97316",

color:"white"

}}

>

Update Password

</Button>



</DialogActions>



</Dialog>








</Box>

);


}










function Info({label,value}){


return(

<Box

display="flex"

mt={2}

>


<Typography

color="#94a3b8"

width={130}

>

{label}

</Typography>




<Typography>

{value}

</Typography>


</Box>

);


}










const fieldStyle={


input:{

color:"white"

},


label:{

color:"#94a3b8"

},


"& fieldset":{

borderColor:"#334155"

},


"& svg":{

color:"white"

}


};







export default Profile;