import {

    Box,

    Typography

} from "@mui/material";



import {

    Dashboard,

    Videocam,

    Psychology,

    Notifications,

    Link,

    Logout,

    People,

    AccountCircle,

    AdminPanelSettings

} from "@mui/icons-material";



import {

    NavLink,

    useNavigate

} from "react-router-dom";



import logo from "../assets/HMEL_Logo.jpg";



import { useAuth } from "../context/AuthContext";









function Sidebar(){



const navigate = useNavigate();



const {user, logout}=useAuth();










// ============================
// Permission Check
// ============================

const hasPermission=(permission)=>{



    if(user?.is_super_admin){


        return true;


    }




    return user?.permissions?.includes(

        permission

    );


};









// ============================
// MENU
// ============================

const menu=[



{

name:"Dashboard",

path:"/",

icon:<Dashboard/>,

permission:"view_dashboard"

},








{

name:"Cameras",

path:"/cameras",

icon:<Videocam/>,

permission:"view_cameras"

},








{

name:"AI Models",

path:"/models",

icon:<Psychology/>,

permission:"view_models"

},









{

name:"Mapping",

path:"/mapping",

icon:<Link/>,

permission:"manage_mapping"

},









{

name:"Alerts",

path:"/alerts",

icon:<Notifications/>,

permission:"view_alerts"

},









{

name:"Users",

path:"/users",

icon:<People/>,

permission:"view_users"

},







{

name:"Roles",

path:"/roles",

icon:<AdminPanelSettings/>,

permission:"view_roles"

},








// profile always visible

{

name:"Profile",

path:"/profile",

icon:<AccountCircle/>,

permission:null

}



];












// ============================
// Logout
// ============================

const handleLogout=()=>{



logout();



navigate(

    "/login"

);



};









return(

<Box

sx={{

width:260,

height:"100vh",

background:"#0d0f12",

borderRight:"1px solid #1f2937",

color:"white",

display:"flex",

flexDirection:"column"

}}

>











{/* LOGO */}



<Box

sx={{

p:3,

display:"flex",

alignItems:"center",

gap:2

}}

>



<Box

component="img"

src={logo}

sx={{

width:55,

background:"white",

borderRadius:1,

p:.5

}}

/>





<Typography

fontWeight={900}

>

HMEL Vision

</Typography>



</Box>














{/* MENU */}



<Box

sx={{

flex:1,

mt:3

}}

>



{


menu


.filter(item=>{


    if(item.permission===null){


        return true;


    }




    return hasPermission(

        item.permission

    );


})


.map(item=>(



<NavLink


key={item.name}


to={item.path}


style={{


textDecoration:"none"


}}

>




{({isActive})=>(



<Box

sx={{

mx:2,

mb:1,

p:1.5,

display:"flex",

gap:2,

alignItems:"center",

borderRadius:2,

color:"white",



background:

isActive

?

"#f97316"

:

"transparent",



"&:hover":{


background:

isActive

?

"#f97316"

:

"#161b22"


}



}}

>



{item.icon}


{item.name}



</Box>



)}




</NavLink>



))


}




</Box>














{/* LOGOUT */}


<Box

onClick={handleLogout}

sx={{

m:2,

p:1.5,

display:"flex",

gap:2,

cursor:"pointer",

borderRadius:2,

"&:hover":{

background:"#161b22"

}

}}

>



<Logout/>


Logout



</Box>








</Box>


);


}









export default Sidebar;