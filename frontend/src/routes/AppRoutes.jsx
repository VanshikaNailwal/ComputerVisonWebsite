import {

    Routes,
    Route,
    Navigate

} from "react-router-dom";


import {

    useEffect,
    useState

} from "react";



import Login from "../pages/auth/Login";

import Register from "../pages/auth/Register";

import ForgotPassword from "../pages/auth/ForgotPassword";

import ResetPassword from "../pages/auth/ResetPassword";



import Setup from "../pages/Setup";



import Dashboard from "../pages/dashboard/Dashboard";


import Cameras from "../pages/Cameras";

import Models from "../pages/Models";

import Mapping from "../pages/Mapping";

import Alerts from "../pages/Alerts";

import Users from "../pages/Users";

import Roles from "../pages/Roles";

import Profile from "../pages/Profile";




import Layout from "../components/Layout";


import { useAuth } from "../context/AuthContext";


import {

    checkSetupStatus

} from "../api/setupApi";











// ==========================
// CHECK LOGIN
// ==========================

const ProtectedRoute = ({

    children

})=>{


const {user}=useAuth();



if(!user){


    return <Navigate to="/login"/>;


}



return children;


};










// ==========================
// PERMISSION SECURITY
// ==========================

const PermissionRoute = ({

    children,

    permission

})=>{


const {user}=useAuth();




// Super admin bypass

if(user?.is_super_admin){


    return children;


}





if(

    !user?.permissions?.includes(

        permission

    )

){


    return <Navigate to="/"/>;


}





return children;


};












// ==========================
// APP ROUTES
// ==========================

function AppRoutes(){



const [loading,setLoading]=useState(true);


const [setupRequired,setSetupRequired]=useState(false);







useEffect(()=>{


const check=async()=>{


try{


const result = await checkSetupStatus();



setSetupRequired(

    result.setup_required

);



}

catch(error){


console.log(

    "Setup check failed",

    error

);


}



setLoading(false);



};



check();



},[]);








if(loading){


return (

<div>

Loading...

</div>

);


}











return(

<Routes>







{/* =======================
    FIRST INSTALL SETUP
======================= */}


<Route

path="/setup"

element={

setupRequired

?

<Setup/>

:

<Navigate to="/login"/>

}

/>









{/* PUBLIC */}


<Route

path="/login"

element={

setupRequired

?

<Navigate to="/setup"/>

:

<Login/>

}

/>





<Route

path="/register"

element={

setupRequired

?

<Navigate to="/setup"/>

:

<Register/>

}

/>





<Route

path="/forgot-password"

element={<ForgotPassword/>}

/>



<Route

path="/reset-password"

element={<ResetPassword/>}

/>










{/* PROTECTED */}

<Route


path="/"


element={


setupRequired

?

<Navigate to="/setup"/>

:

(

<ProtectedRoute>


<Layout/>


</ProtectedRoute>

)


}


>









{/* ANY LOGIN USER */}

<Route

index

element={<Dashboard/>}

/>




<Route

path="profile"

element={<Profile/>}

/>










{/* ALERTS */}

<Route

path="alerts"

element={


<PermissionRoute permission="view_alerts">


<Alerts/>


</PermissionRoute>


}

/>










{/* CAMERAS */}

<Route


path="cameras"


element={


<PermissionRoute permission="view_cameras">


<Cameras/>


</PermissionRoute>


}


/>










{/* AI MODELS */}

<Route


path="models"


element={


<PermissionRoute permission="view_models">


<Models/>


</PermissionRoute>


}


/>










{/* MODEL CAMERA MAPPING */}

<Route


path="mapping"


element={


<PermissionRoute permission="manage_mapping">


<Mapping/>


</PermissionRoute>


}


/>











{/* USERS */}

<Route


path="users"


element={


<PermissionRoute permission="view_users">


<Users/>


</PermissionRoute>


}


/>










{/* ROLES */}

<Route


path="roles"


element={


<PermissionRoute permission="view_roles">


<Roles/>


</PermissionRoute>


}


/>









</Route>



</Routes>

);



}







export default AppRoutes;