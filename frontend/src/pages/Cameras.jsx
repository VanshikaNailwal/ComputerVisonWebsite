import { useEffect, useState } from "react";


import {

Box,
Typography,
Paper,
Button,
Table,
TableHead,
TableRow,
TableCell,
TableBody,
Chip,
Dialog,
DialogTitle,
DialogContent,
TextField,
DialogActions,
IconButton,
CircularProgress

} from "@mui/material";


import {

Add,
Delete,
Edit,
Sensors

} from "@mui/icons-material";


import api from "../api/axios";


import { useAuth } from "../context/AuthContext";










function Cameras(){



const {user}=useAuth();





// =====================
// PERMISSION CHECK
// =====================

const canManageCameras =

user?.is_super_admin

||

user?.permissions?.includes(

"manage_cameras"

);









const [cameras,setCameras]=useState([]);


const [open,setOpen]=useState(false);


const [editId,setEditId]=useState(null);


const [error,setError]=useState("");


const [testing,setTesting]=useState(null);







const [form,setForm]=useState({


name:"",

ip_address:"",

location:"",

rtsp_url:""

});











// =====================
// LOAD CAMERAS
// =====================

const loadCameras=async()=>{


try{


const res=await api.get(

"/cameras"

);



setCameras(

res.data

);



}

catch(error){


console.log(error);


}


};









useEffect(()=>{


loadCameras();




const interval=setInterval(()=>{


loadCameras();


},10000);




return ()=>clearInterval(interval);



},[]);











// =====================
// INPUT CHANGE
// =====================

const handleChange=(e)=>{


setForm({

...form,

[e.target.name]:e.target.value

});


};











// =====================
// SAVE CAMERA
// =====================

const saveCamera=async()=>{


if(!canManageCameras)

return;





try{


setError("");




if(editId){



await api.patch(

`/cameras/${editId}`,

form

);



}

else{



await api.post(

"/cameras",

form

);



}





await loadCameras();



closeDialog();



}

catch(error){



setError(

error.response?.data?.detail ||

"Operation failed"

);



}



};












// =====================
// TEST CAMERA
// =====================

const testCamera=async(id)=>{



if(!canManageCameras)

return;





try{



setTesting(id);




setCameras(prev=>

prev.map(cam=>

cam.id===id

?

{

...cam,

connection_status:"CHECKING"

}

:

cam

)

);








const res=await api.get(

`/cameras/${id}/test`

);








setCameras(prev=>

prev.map(cam=>


cam.id===id

?

{

...cam,

connection_status:

res.data.connection_status

}

:

cam


)

);



}

catch(error){


console.log(error);


}

finally{


setTesting(null);


}



};











// =====================
// EDIT CAMERA
// =====================

const editCamera=(camera)=>{



if(!canManageCameras)

return;





setEditId(

camera.id

);





setForm({


name:camera.name,


ip_address:camera.ip_address,


location:camera.location,


rtsp_url:camera.rtsp_url


});





setOpen(true);



};











// =====================
// DELETE CAMERA
// =====================

const deleteCamera=async(id)=>{



if(!canManageCameras)

return;






const confirmDelete=window.confirm(

"Delete this camera?"

);



if(!confirmDelete)

return;







await api.delete(

`/cameras/${id}`

);





loadCameras();



};












const closeDialog=()=>{



setOpen(false);


setEditId(null);


setError("");



setForm({


name:"",

ip_address:"",

location:"",

rtsp_url:""


});



};












// =====================
// STATUS
// =====================

const statusChip=(status)=>{



if(status==="ONLINE")


return {

label:"🟢 Connected",

color:"#16a34a"

};





if(status==="OFFLINE")


return {

label:"🔴 Disconnected",

color:"#dc2626"

};





return {


label:"🟡 Checking...",


color:"#ca8a04"


};



};









return(

<Box

sx={{

p:3,

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

mb={3}

>


<Box>


<Typography

variant="h4"

fontWeight={900}

>

Camera Management

</Typography>




<Typography color="#94a3b8">

Manage RTSP Camera Streams

</Typography>



</Box>









{

canManageCameras &&


<Button

startIcon={<Add/>}

onClick={()=>setOpen(true)}

sx={orangeBtn}

>

Add Camera

</Button>


}




</Box>









{/* TABLE */}


<Paper

sx={{

background:"#111827",

borderRadius:3,

overflow:"hidden"

}}

>


<Table>


<TableHead>


<TableRow>



{


[

"Name",

"IP",

"Location",

"RTSP",

"Connection",

...(canManageCameras ? ["Actions"] : [])

].map(x=>(



<TableCell

key={x}

sx={head}

>

{x}

</TableCell>


))


}




</TableRow>


</TableHead>










<TableBody>


{


cameras.map(cam=>{



const status=statusChip(

cam.connection_status

);






return(

<TableRow key={cam.id}>




<TableCell sx={cell}>

{cam.name}

</TableCell>



<TableCell sx={cell}>

{cam.ip_address}

</TableCell>



<TableCell sx={cell}>

{cam.location}

</TableCell>




<TableCell sx={cell}>

{cam.rtsp_url}

</TableCell>







<TableCell>


<Chip

label={status.label}

sx={{

background:status.color,

color:"white",

fontWeight:700

}}

/>


</TableCell>










{


canManageCameras &&


<TableCell>






<Button

startIcon={

testing===cam.id

?

<CircularProgress size={18}/>

:

<Sensors/>

}

disabled={testing===cam.id}

onClick={()=>testCamera(cam.id)}

sx={{

mr:1,

background:"#2563eb",

color:"white"

}}

>

Test

</Button>










<IconButton

onClick={()=>editCamera(cam)}

>


<Edit sx={{color:"#38bdf8"}}/>


</IconButton>







<IconButton

onClick={()=>deleteCamera(cam.id)}

>


<Delete sx={{color:"#ef4444"}}/>


</IconButton>





</TableCell>


}




</TableRow>

)


})


}



</TableBody>



</Table>


</Paper>









{/* DIALOG */}


<Dialog

open={open}

onClose={closeDialog}

PaperProps={{

sx:{

background:"#111827",

color:"white",

width:500

}

}}

>


<DialogTitle>


{editId?"Edit Camera":"Add Camera"}


</DialogTitle>






<DialogContent>


{


[

["Camera Name","name"],

["IP Address","ip_address"],

["Location","location"],

["RTSP URL","rtsp_url"]

].map(field=>(



<TextField

key={field[1]}

fullWidth

margin="normal"

label={field[0]}

name={field[1]}

value={form[field[1]]}

onChange={handleChange}

sx={input}

/>



))


}





<Typography color="error">

{error}

</Typography>




</DialogContent>






<DialogActions>



<Button

onClick={closeDialog}

>

Cancel

</Button>




<Button

onClick={saveCamera}

sx={orangeBtn}

>

{editId?"Update":"Save"}

</Button>



</DialogActions>



</Dialog>








</Box>

);


}









const head={

color:"#94a3b8",

fontWeight:700

};





const cell={

color:"white",

maxWidth:250,

overflow:"hidden",

textOverflow:"ellipsis"

};








const input={


"& label":{

color:"#94a3b8"

},


"& input":{

color:"white"

},


"& fieldset":{

borderColor:"#334155"

}


};









const orangeBtn={


background:"#f97316",

color:"white",

fontWeight:700,


"&:hover":{

background:"#ea580c"

}


};









export default Cameras;