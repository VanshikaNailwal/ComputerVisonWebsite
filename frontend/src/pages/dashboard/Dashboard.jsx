import { useAuth } from "../../context/AuthContext";


import AdminDashboard from "./AdminDashboard";


import OperatorDashboard from "./OperatorDashboard";









function Dashboard(){



const {user}=useAuth();







// --------------------------------
// SUPER ADMIN
// --------------------------------

if(user?.is_super_admin){



    return (

        <AdminDashboard/>

    );


}









// --------------------------------
// ADMIN TYPE DASHBOARD
//
// Anyone who manages system
// resources gets admin dashboard
// --------------------------------

const adminPermissions = [

    "manage_users",

    "manage_roles",

    "manage_cameras",

    "manage_models",

    "manage_mapping"

];








const isAdminType = adminPermissions.some(

    permission =>

    user?.permissions?.includes(

        permission

    )

);









if(isAdminType){



    return (

        <AdminDashboard/>

    );


}









// --------------------------------
// DEFAULT MONITORING DASHBOARD
// --------------------------------

return (

    <OperatorDashboard/>

);




}









export default Dashboard;