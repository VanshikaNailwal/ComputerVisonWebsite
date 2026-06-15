import { useEffect, useState } from "react";


import {

Box,
Typography,
Paper,
Table,
TableHead,
TableRow,
TableCell,
TableBody,
Select,
MenuItem,
IconButton,
Dialog,
DialogTitle,
DialogContent,
DialogActions,
Button,
Grid,
TextField,
Divider,
TablePagination

} from "@mui/material";


import {

Visibility,
Delete

} from "@mui/icons-material";


import { useAuth } from "../context/AuthContext";


import {

getEvents,
deleteEvent,
updateEventStatus

} from "../api/eventsApi";









function Alerts(){



const {user}=useAuth();





const canManageAlerts =

user?.is_super_admin

||

user?.permissions?.includes(

"manage_alerts"

);









const [alerts,setAlerts]=useState([]);

const [total,setTotal]=useState(0);

const [page,setPage]=useState(0);

const rowsPerPage=20;



const [selectedEvent,setSelectedEvent]=useState(null);



const [statusDialog,setStatusDialog]=useState(false);

const [selectedAlert,setSelectedAlert]=useState(null);

const [newStatus,setNewStatus]=useState("");

const [note,setNote]=useState("");








const [filters,setFilters]=useState({

camera:"ALL",

model:"ALL",

status:"ALL",

fromDate:"",

toDate:"",

fromTime:"",

toTime:""

});









const loadEvents=async()=>{


try{


const response=await getEvents(

page+1,

rowsPerPage

);



setAlerts(

response.data

);



setTotal(

response.total

);



}

catch(error){


console.log(

"Events failed",

error

);


}


};








useEffect(()=>{


loadEvents();



const timer=setInterval(

loadEvents,

3000

);



return ()=>clearInterval(timer);



},[page]);











const handleDelete=async(id)=>{


if(!canManageAlerts)

return;



await deleteEvent(id);


loadEvents();


};









const openStatusDialog=(alert,status)=>{


if(!canManageAlerts)

return;




setSelectedAlert(alert);

setNewStatus(status);

setNote("");

setStatusDialog(true);


};









const submitStatusUpdate=async()=>{


if(

newStatus!=="ACTIVE"

&&

note.trim()===""

){


alert(

"Please enter remarks"

);


return;


}





await updateEventStatus(

selectedAlert.id,

{

status:newStatus,

resolution_note:note,

resolved_by:user?.email || "SYSTEM"

}

);




setStatusDialog(false);


loadEvents();


};











const cameras=[

"ALL",

...new Set(

alerts.map(a=>a.camera_name).filter(Boolean)

)

];



const models=[

"ALL",

...new Set(

alerts.map(a=>a.model_name).filter(Boolean)

)

];









const filteredAlerts=alerts.filter(a=>{


const date=a.created_at?.split("T")[0];

const time=a.created_at?.split("T")[1]?.slice(0,5);



return(

(filters.camera==="ALL" || a.camera_name===filters.camera)

&&

(filters.model==="ALL" || a.model_name===filters.model)

&&

(filters.status==="ALL" || (a.status||"ACTIVE")===filters.status)

&&

(!filters.fromDate || date>=filters.fromDate)

&&

(!filters.toDate || date<=filters.toDate)

&&

(!filters.fromTime || time>=filters.fromTime)

&&

(!filters.toTime || time<=filters.toTime)

);


});

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

<Typography

variant="h4"

fontWeight={900}

>

{

canManageAlerts

?

"All Alerts"

:

"My Alerts"

}

</Typography>




<Typography

color="#94a3b8"

mb={3}

>

Live AI Detection Alerts

</Typography>









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

"ID",

"Camera",

"Model",

"Detection",

"Confidence",

"Evidence",

"Status",

"Date",

"Time",

...(canManageAlerts?["Action"]:[])

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


filteredAlerts.map(alert=>{



const date=alert.created_at?.split("T")[0];


const time=alert.created_at?.split("T")[1]?.slice(0,5);




return(

<TableRow key={alert.id}>


<TableCell sx={cell}>

{alert.id}

</TableCell>



<TableCell sx={cell}>

{alert.camera_name}

</TableCell>




<TableCell sx={cell}>

{alert.model_name}

</TableCell>




<TableCell sx={cell}>

{alert.label}

</TableCell>





<TableCell sx={cell}>

{Math.round(alert.confidence*100)}%

</TableCell>








{/* EVIDENCE BUTTON */}


<TableCell>


<IconButton

onClick={()=>setSelectedEvent(alert)}

>


<Visibility sx={{color:"#38bdf8"}}/>


</IconButton>


</TableCell>









{/* STATUS */}


<TableCell>


<Select

size="small"

value={alert.status || "ACTIVE"}

disabled={!canManageAlerts}

sx={selectStyle}

MenuProps={menuStyle}

onChange={(e)=>

openStatusDialog(

alert,

e.target.value

)

}

>


{


[

"ACTIVE",

"RESOLVED",

"FALSE ALARM"

].map(s=>(


<MenuItem

key={s}

value={s}

>

{s}

</MenuItem>


))


}


</Select>


</TableCell>







<TableCell sx={cell}>

{date}

</TableCell>



<TableCell sx={cell}>

{time}

</TableCell>








{

canManageAlerts &&


<TableCell>


<IconButton

onClick={()=>handleDelete(alert.id)}

>


<Delete sx={{color:"#ef4444"}}/>


</IconButton>


</TableCell>

}



</TableRow>


);


})


}


</TableBody>


</Table>








{/* PAGINATION */}


<TablePagination

component="div"

count={total}

page={page}

rowsPerPage={rowsPerPage}

rowsPerPageOptions={[20]}

onPageChange={(e,newPage)=>setPage(newPage)}

sx={{

color:"white",

".MuiSvgIcon-root":{

color:"white"

}

}}

/>



</Paper>









{/* ALERT DETAILS POPUP */}

<Dialog

open={Boolean(selectedEvent)}

onClose={()=>setSelectedEvent(null)}

maxWidth="md"

fullWidth

PaperProps={{

sx:{

background:"#111827",

color:"white"

}

}}

>


{


selectedEvent &&


<>


<DialogTitle>

Alert Details

</DialogTitle>





<DialogContent>



<Typography>

Camera : {selectedEvent.camera_name}

</Typography>




<Typography>

Model : {selectedEvent.model_name}

</Typography>



<Typography>

Detection : {selectedEvent.label}

</Typography>




<Typography>

Confidence : {Math.round(selectedEvent.confidence*100)}%

</Typography>









{/* IMAGE DISPLAY */}


{


selectedEvent.image_path

?


<>


<Divider sx={{my:2,borderColor:"#334155"}}/>




<img

src={

`http://localhost:8000/${

selectedEvent.image_path.replaceAll(

"\\",

"/"

)

}`

}

alt="Evidence"

onError={(e)=>{


console.log(

"Image failed:",

e.target.src

);


}}

style={{

width:"100%",

maxHeight:"500px",

objectFit:"contain",

borderRadius:"12px"

}}

/>



</>


:


<Typography

color="#f97316"

mt={2}

>

No Evidence Image Available

</Typography>


}









<Divider sx={{my:2,borderColor:"#334155"}}/>




<Typography>

Status : {selectedEvent.status}

</Typography>




<Typography>

Resolved By : {selectedEvent.resolved_by || "-"}

</Typography>




<Typography>

Remarks : {selectedEvent.resolution_note || "-"}

</Typography>





</DialogContent>


</>


}


</Dialog>










{/* STATUS POPUP */}


<Dialog

open={statusDialog}

onClose={()=>setStatusDialog(false)}

>


<DialogTitle>

Update Alert Status

</DialogTitle>




<DialogContent>


<TextField

label="Remarks"

multiline

rows={4}

fullWidth

value={note}

onChange={(e)=>setNote(e.target.value)}

/>


</DialogContent>





<DialogActions>


<Button onClick={()=>setStatusDialog(false)}>

Cancel

</Button>



<Button

variant="contained"

onClick={submitStatusUpdate}

>

Update

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

color:"white"

};





const selectStyle={

background:"#1e293b",

color:"white",

borderRadius:"8px",

"& svg":{

color:"white"

}

};




const inputStyle={

background:"#1e293b",

borderRadius:"8px",

"& input":{

color:"white"

},

"& label":{

color:"#cbd5e1"

}

};




const menuStyle={

PaperProps:{

sx:{

background:"#1e293b",

color:"white"

}

}

};





export default Alerts;