import { useEffect, useState } from "react";


import {

    Box,
    Typography,
    Grid,
    Paper,
    Table,
    TableHead,
    TableRow,
    TableCell,
    TableBody,
    Chip,
    CircularProgress

} from "@mui/material";


import {

    Videocam,
    Psychology,
    Notifications,
    People,
    CheckCircle,
    Error

} from "@mui/icons-material";


import {

    getAdminDashboard

} from "../../api/dashboardApi";









function AdminDashboard(){


const [data,setData]=useState(null);









const loadDashboard=async()=>{


try{


const response=await getAdminDashboard();


setData(response);



}

catch(error){


console.log(

"Dashboard error",

error

);


}



};









useEffect(()=>{


loadDashboard();



const timer=setInterval(

()=>loadDashboard(),

10000

);



return ()=>clearInterval(timer);



},[]);










if(!data){


return(

<Box

sx={{

height:"100vh",

display:"flex",

alignItems:"center",

justifyContent:"center",

background:"#0f172a"

}}

>

<CircularProgress/>

</Box>

);


}










return(

<Box

sx={{

p:4,

background:"#0f172a",

minHeight:"100vh",

color:"white"

}}

>









<Typography

variant="h4"

fontWeight={900}

color="white"

>

Admin Dashboard

</Typography>



<Typography

color="#94a3b8"

mb={4}

>

HMEL AI Vision Monitoring System

</Typography>










{/* CARDS */}


<Grid container spacing={3} mb={4}>



<Card

title="Total Cameras"

value={data?.cameras?.total}

icon={<Videocam/>}

/>



<Card

title="Online Cameras"

value={data?.cameras?.online}

icon={<CheckCircle/>}

color="#22c55e"

/>



<Card

title="Offline Cameras"

value={data?.cameras?.offline}

icon={<Error/>}

color="#ef4444"

/>




<Card

title="AI Models"

value={data?.models?.total}

icon={<Psychology/>}

/>




<Card

title="Operators"

value={data?.users?.total}

icon={<People/>}

/>




<Card

title="Active Alerts"

value={data?.alerts?.active}

icon={<Notifications/>}

color="#f97316"

/>




<Card

title="Resolved Alerts"

value={data?.alerts?.resolved}

icon={<CheckCircle/>}

color="#22c55e"

/>



<Card

title="False Alarms"

value={data?.alerts?.false_alarm}

icon={<Error/>}

color="#eab308"

/>




<Card

title="Total Alerts"

value={data?.alerts?.total}

icon={<Notifications/>}

/>


</Grid>










{/* RECENT ALERTS */}


<Paper

sx={{

background:"#111827",

borderRadius:4,

border:"1px solid #334155",

overflow:"hidden"

}}

>


<Box p={3}>


<Typography

fontSize={22}

fontWeight={900}

color="white"

>

Recent Alerts

</Typography>


</Box>







<Table>


<TableHead>


<TableRow>


{

[

"Camera",

"Model",

"Detection",

"Status",

"Time"


].map(h=>(


<TableCell

key={h}

sx={head}

>

{h}

</TableCell>


))


}



</TableRow>


</TableHead>








<TableBody>


{


data?.recent_alerts?.map(alert=>(


<TableRow

key={alert.id}

hover

>


<TableCell sx={cell}>

{alert.camera}

</TableCell>



<TableCell sx={cell}>

{alert.model}

</TableCell>



<TableCell sx={cell}>

{alert.type}

</TableCell>





<TableCell sx={cell}>


<Chip


label={alert.status}


sx={{

fontWeight:800,

color:"white",

background:

alert.status==="ACTIVE"

?

"#dc2626"

:

alert.status==="RESOLVED"

?

"#16a34a"

:

"#ca8a04"


}}


/>


</TableCell>





<TableCell sx={cell}>

{

new Date(alert.time).toLocaleString()

}

</TableCell>



</TableRow>


))


}



</TableBody>



</Table>



</Paper>





</Box>


);


}










function Card({

title,

value=0,

icon,

color="#38bdf8"

}){


return(

<Grid item xs={12} md={4}>


<Paper

sx={{

height:120,

background:

"linear-gradient(145deg,#111827,#0b1220)",

border:"1px solid #334155",

borderRadius:4,

p:3

}}

>



<Box

display="flex"

justifyContent="space-between"

alignItems="center"

height="100%"

>



<Box>



<Typography

color="#94a3b8"

fontSize={17}

>

{title}

</Typography>




<Typography

variant="h3"

fontWeight={900}

color="white"

>

{value || 0}

</Typography>



</Box>





<Box

sx={{

color,

"& svg":{

fontSize:35

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










const head={

color:"#93c5fd",

fontWeight:900,

fontSize:16,

borderColor:"#334155"

};



const cell={

color:"white",

fontWeight:600,

fontSize:15,

borderColor:"#334155"

};







export default AdminDashboard;