import { useState } from "react";


import {

    Box,
    TextField,
    Button,
    Typography,
    Paper,
    Alert,
    MenuItem

} from "@mui/material";


import { useNavigate } from "react-router-dom";


import {

    createSuperAdmin

} from "../api/setupApi";









function Setup(){



const navigate = useNavigate();





const departments=[

    "IT",

    "Operations",

    "Safety",

    "Maintenance"

];






const [form,setForm]=useState({

    employee_id:"",

    name:"",

    email:"",

    phone_number:"",

    department:"",

    password:""

});





const [error,setError]=useState("");

const [success,setSuccess]=useState("");









const handleChange=(e)=>{


    setForm({

        ...form,


        [e.target.name]:e.target.value

    });


};









const submit=async()=>{


try{


    setError("");



    if(

        !form.employee_id ||

        !form.name ||

        !form.email ||

        !form.phone_number ||

        !form.department ||

        !form.password

    ){


        setError(

            "Please fill all fields"

        );


        return;

    }








    await createSuperAdmin(

        form

    );








    setSuccess(

        "Super Admin Created Successfully"

    );







    setTimeout(()=>{


        navigate(

            "/login"

        );


        window.location.reload();


    },1000);




}

catch(error){



    console.log(

        error

    );




    setError(

        error.response?.data?.detail

        ||

        "Failed to create super admin"

    );


}



};









return(

<Box

sx={{

    height:"100vh",

    background:"#0f172a",

    display:"flex",

    justifyContent:"center",

    alignItems:"center"

}}

>




<Paper

sx={{

    width:450,

    p:4,

    background:"#111827",

    color:"white",

    borderRadius:3

}}

>





<Typography

variant="h4"

fontWeight={900}

>

HMEL Vision Setup

</Typography>





<Typography

color="#94a3b8"

mb={3}

>

Create First Super Administrator

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

label="Employee ID"

name="employee_id"

value={form.employee_id}

onChange={handleChange}

fullWidth

sx={inputStyle}

/>







<TextField

label="Full Name"

name="name"

value={form.name}

onChange={handleChange}

fullWidth

sx={inputStyle}

/>







<TextField

label="Company Email"

name="email"

value={form.email}

onChange={handleChange}

fullWidth

sx={inputStyle}

/>








<TextField

label="Phone Number"

name="phone_number"

value={form.phone_number}

onChange={handleChange}

fullWidth

sx={inputStyle}

/>









<TextField

select

label="Department"

name="department"

value={form.department}

onChange={handleChange}

fullWidth

sx={inputStyle}

>


{


departments.map(dept=>(


<MenuItem

key={dept}

value={dept}

>

{dept}

</MenuItem>


))


}


</TextField>








<TextField

label="Password"

name="password"

type="password"

value={form.password}

onChange={handleChange}

fullWidth

sx={inputStyle}

/>








<Button

variant="contained"

fullWidth

sx={{

    mt:2,

    height:50,

    fontWeight:800

}}

onClick={submit}

>

Create Super Admin

</Button>





</Paper>



</Box>

);


}









const inputStyle={


    mb:2,


    input:{

        color:"white"

    },


    "& .MuiSelect-select":{

        color:"white"

    },


    "& svg":{

        color:"white"

    },


    label:{

        color:"#94a3b8"

    },


    "& .MuiOutlinedInput-root":{


        "& fieldset":{

            borderColor:"#334155"

        },


        "&:hover fieldset":{

            borderColor:"#38bdf8"

        }


    }


};








export default Setup;