import {

Box

} from "@mui/material";


import {

Outlet

} from "react-router-dom";


import Sidebar from "./Sidebar";








function Layout(){



return (


<Box

sx={{

width:"100vw",

height:"100vh",

display:"flex",

background:"#0d0f12",

overflow:"hidden"

}}

>


<Sidebar/>





<Box

sx={{

flex:1,

height:"100vh",

overflowY:"auto",

background:"#0f172a"

}}

>


<Outlet/>


</Box>




</Box>


);


}





export default Layout;