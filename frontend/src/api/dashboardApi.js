import api from "./axios";






// ----------------------------------
// Admin Dashboard
// ----------------------------------

export const getAdminDashboard = async()=>{


    const response = await api.get(

        "/dashboard/admin"

    );



    return response.data;


};









// ----------------------------------
// Operator Dashboard
// ----------------------------------

export const getOperatorDashboard = async()=>{


    const response = await api.get(

        "/dashboard/operator"

    );



    return response.data;


};