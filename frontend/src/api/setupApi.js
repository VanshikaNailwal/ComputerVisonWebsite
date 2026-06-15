import axios from "axios";


const API_URL = "http://localhost:8000";



// check first installation

export const checkSetupStatus = async()=>{


    const response = await axios.get(

        `${API_URL}/setup/status`

    );


    return response.data;

};





// create first super admin

export const createSuperAdmin = async(data)=>{


    const response = await axios.post(

        `${API_URL}/setup/create-admin`,

        data

    );


    return response.data;

};