import { useEffect, useState } from "react";


import {

    Box,
    Typography,
    Grid,
    Paper,
    Chip,
    Button,
    LinearProgress,
    CircularProgress

} from "@mui/material";



import {

    Warning,
    CheckCircle,
    Error,
    Visibility

} from "@mui/icons-material";



import {

    useNavigate

} from "react-router-dom";



import {

    getOperatorDashboard

} from "../../api/dashboardApi";









function OperatorDashboard(){



const [data,setData]=useState(null);



const navigate=useNavigate();










// ============================
// LOAD DASHBOARD
// ============================

const loadDashboard=async()=>{



try{



const response = await getOperatorDashboard();



setData(

    response

);



}

catch(error){



console.log(

    "Operator Dashboard Error",

    error

);



}



};










useEffect(()=>{



loadDashboard();




const interval=setInterval(

    ()=>loadDashboard(),

    5000

);




return ()=>clearInterval(interval);



},[]);










// ============================
// LOADING
// ============================

if(!data){



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


<CircularProgress/>


</Box>

);



}










const latestAlerts = (

    data.active_alerts || []

).slice(0,9);









return(

<Box

sx={{

p:4,

background:"#0f172a",

minHeight:"100vh",

color:"white"

}}

>











{/* HEADER */}


<Box

display="flex"

justifyContent="space-between"

alignItems="center"

mb={4}

>


<Box>


<Typography

variant="h4"

fontWeight={900}

color="white"

>

Operator Dashboard

</Typography>



<Typography

color="#94a3b8"

>

Live Safety Monitoring Console

</Typography>


</Box>






<Button

variant="contained"

onClick={()=>navigate("/alerts")}

sx={{

background:"#f97316",

fontWeight:800

}}

>

View All Alerts

</Button>



</Box>













{/* SUMMARY */}


<Grid container spacing={3} mb={4}>





<StatusCard

title="Active Alerts"

value={data?.summary?.active || 0}

icon={<Warning/>}

color="#ef4444"

/>





<StatusCard

title="Resolved"

value={data?.summary?.resolved || 0}

icon={<CheckCircle/>}

color="#22c55e"

/>





<StatusCard

title="False Alarms"

value={data?.summary?.false_alarm || 0}

icon={<Error/>}

color="#eab308"

/>




</Grid>












<Typography

fontSize={24}

fontWeight={900}

mb={3}

color="white"

>

Latest Active Incidents

</Typography>










<Grid container spacing={3}>


{


latestAlerts.length>0

?

latestAlerts.map(alert=>(




<Grid

item

xs={12}

md={4}

key={alert.id}

>



<Paper

sx={{

background:

"linear-gradient(145deg,#111827,#0b1220)",

border:"1px solid #334155",

borderRadius:4,

p:3

}}

>







<Typography

fontSize={22}

fontWeight={900}

color="white"

mb={2}

>

🚨 {alert.type}

</Typography>










<Info

title="Camera"

value={alert.camera}

/>



<Info

title="AI Model"

value={alert.model}

/>










<Typography

color="#94a3b8"

mt={2}

>

Confidence

</Typography>



<Typography

color="white"

fontWeight={800}

>

{Math.round(alert.confidence*100)}%

</Typography>





<LinearProgress

variant="determinate"

value={alert.confidence*100}

sx={{

mt:1,

height:8,

borderRadius:5

}}

/>










<Chip

label="ACTIVE"

sx={{

mt:3,

background:"#dc2626",

color:"white",

fontWeight:900

}}

/>










<Button

fullWidth

startIcon={<Visibility/>}

onClick={()=>navigate("/alerts")}

sx={{

mt:3,

background:"#f97316",

color:"white",

fontWeight:900

}}

>

View Details

</Button>







</Paper>


</Grid>



))


:


<Typography

color="#94a3b8"

ml={3}

>

No active incidents 🎉

</Typography>


}



</Grid>






</Box>


);



}











// ============================
// INFO FIELD
// ============================

function Info({

title,

value

}){



return(

<Box mt={2}>


<Typography

color="#94a3b8"

>

{title}

</Typography>



<Typography

color="white"

fontWeight={700}

>

{value}

</Typography>


</Box>

);



}











// ============================
// SUMMARY CARD
// ============================

function StatusCard({

title,

value,

icon,

color

}){


return(

<Grid item xs={12} md={4}>


<Paper

sx={{

background:"#111827",

border:"1px solid #334155",

borderRadius:4,

p:3

}}

>


<Box

display="flex"

justifyContent="space-between"

alignItems="center"

>


<Box>


<Typography

color="#94a3b8"

fontSize={18}

>

{title}

</Typography>




<Typography

variant="h3"

fontWeight={900}

color="white"

>

{value}

</Typography>


</Box>





<Box

sx={{

color,

"& svg":{

fontSize:40

}

}}

>

{icon}

</Box>




</Box>



</Paper>


</Grid>


);


}










export default OperatorDashboard;