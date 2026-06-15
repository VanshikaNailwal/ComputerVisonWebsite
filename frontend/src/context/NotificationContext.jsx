import {

createContext,

useContext,

useState

} from "react";



import {

Snackbar,

Alert

} from "@mui/material";






const NotificationContext=createContext();





export const NotificationProvider=({children})=>{


const [notification,setNotification]=useState({


open:false,


message:"",


severity:"success"


});






const showNotification=(message,severity="success")=>{


setNotification({

open:true,

message,

severity

});


};






return (


<NotificationContext.Provider

value={{showNotification}}

>


{children}




<Snackbar


open={notification.open}


autoHideDuration={3000}


onClose={()=>setNotification({...notification,open:false})}


>


<Alert severity={notification.severity}>


{notification.message}


</Alert>



</Snackbar>




</NotificationContext.Provider>


);


};






export const useNotification=()=>{

return useContext(NotificationContext);

};