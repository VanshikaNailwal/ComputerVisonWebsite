import {

    Box,
    Typography

} from "@mui/material";



import {

    CheckCircle,
    Cancel

} from "@mui/icons-material";







function PasswordRules({password}){



const rules=[


{
label:"Minimum 8 characters",
valid:password.length>=8
},


{
label:"One uppercase letter (A-Z)",
valid:/[A-Z]/.test(password)
},


{
label:"One lowercase letter (a-z)",
valid:/[a-z]/.test(password)
},


{
label:"One number (0-9)",
valid:/\d/.test(password)
},


{
label:"One special character (!@#$%^&*)",
valid:/[!@#$%^&*]/.test(password)
}


];






return(

<Box

sx={{

mt:1,

mb:2,

p:2,

borderRadius:2,


background:"#111827",

border:"1px solid #273449"

}}

>



<Typography

fontWeight={800}

mb={1.5}

sx={{

color:"#f97316"

}}

>

Password Requirements

</Typography>






{


rules.map((rule,index)=>(


<Box

key={index}

sx={{

display:"flex",

alignItems:"center",

gap:1,

mb:0.8

}}

>



{


rule.valid

?

<CheckCircle

fontSize="small"

sx={{

color:"#22c55e"

}}

/>


:


<Cancel

fontSize="small"

sx={{

color:"#ef4444"

}}

/>

}




<Typography

variant="body2"

sx={{


color:

rule.valid

?

"#22c55e"

:

"#f87171"


}}

>


{rule.label}


</Typography>



</Box>


))

}




</Box>


);


}





export default PasswordRules;