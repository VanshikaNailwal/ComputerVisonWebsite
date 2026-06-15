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
DialogActions,
Checkbox,
FormControlLabel,
Grid,
IconButton

} from "@mui/material";


import {

Add,
Delete,
Edit

} from "@mui/icons-material";


import api from "../api/axios";


import { useAuth } from "../context/AuthContext";









function Mapping(){



const {user}=useAuth();





// =====================
// PERMISSION CHECK
// =====================

const canManageMapping =

user?.is_super_admin

||

user?.permissions?.includes(

"manage_mapping"

);









const [cameras,setCameras]=useState([]);


const [models,setModels]=useState([]);


const [mappings,setMappings]=useState([]);




const [open,setOpen]=useState(false);



const [selectedCamera,setSelectedCamera]=useState("");


const [selectedModels,setSelectedModels]=useState([]);











// =====================
// LOAD DATA
// =====================

const loadData=async()=>{



try{



const camRes=await api.get(

"/cameras"

);




const modelRes=await api.get(

"/models"

);




const mapRes=await api.get(

"/mapping"

);







setCameras(camRes.data);


setModels(modelRes.data);


setMappings(mapRes.data);



}

catch(error){


console.log(error);


}



};










useEffect(()=>{


loadData();


},[]);











// =====================
// SELECT MODEL
// =====================

const toggleModel=(id)=>{



setSelectedModels(prev=>


prev.includes(id)

?

prev.filter(x=>x!==id)


:


[...prev,id]


);



};












// =====================
// SAVE MAPPING
// =====================

const saveMapping=async()=>{



if(!canManageMapping)

return;






try{



await api.post(

"/mapping",

{

camera_id:selectedCamera,


model_ids:selectedModels

}

);








setOpen(false);



setSelectedCamera("");



setSelectedModels([]);







loadData();




}

catch(error){



console.log(error);



}



};












// =====================
// EDIT
// =====================

const editMapping=(mapping)=>{



if(!canManageMapping)

return;







setSelectedCamera(

mapping.camera_id

);






setSelectedModels(

mapping.models.map(

m=>m.id

)

);






setOpen(true);



};












// =====================
// DELETE
// =====================

const deleteMapping=async(cameraId)=>{



if(!canManageMapping)

return;







const confirmDelete=window.confirm(

"Delete this mapping?"

);




if(!confirmDelete)

return;








try{



await api.delete(

`/mapping/${cameraId}`

);






loadData();




}

catch(error){



console.log(error);



}



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

Camera Model Mapping

</Typography>






<Typography color="#94a3b8">

Assign multiple AI models to cameras

</Typography>



</Box>










{


canManageMapping &&


<Button

startIcon={<Add/>}

onClick={()=>{


setSelectedCamera("");


setSelectedModels([]);


setOpen(true);


}}

sx={orangeBtn}

>

Create Mapping

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

"Camera",

"AI Models",

...(canManageMapping?["Actions"]:[])

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


mappings.map(item=>(



<TableRow key={item.camera_id}>




<TableCell sx={cell}>



{item.camera_name}



</TableCell>









<TableCell sx={cell}>


{


item.models.length>0


?


item.models.map(model=>(



<Chip

key={model.id}

label={model.name}

sx={chip}

/>



))


:


"No Models Assigned"


}


</TableCell>










{


canManageMapping &&


<TableCell>





<IconButton

onClick={()=>editMapping(item)}

>


<Edit sx={{color:"#38bdf8"}}/>


</IconButton>








<IconButton

onClick={()=>deleteMapping(item.camera_id)}

>


<Delete sx={{color:"#ef4444"}}/>


</IconButton>





</TableCell>


}




</TableRow>



))


}



</TableBody>



</Table>



</Paper>













{/* CREATE / EDIT POPUP */}



<Dialog

open={open}

onClose={()=>setOpen(false)}

PaperProps={{

sx:{

background:"#111827",

color:"white",

width:650

}

}}

>





<DialogTitle>

Create Mapping

</DialogTitle>








<DialogContent>



<Grid container spacing={4}>








{/* CAMERAS */}


<Grid item xs={6}>



<Typography fontWeight={800}>

Select Camera

</Typography>







{


cameras.map(cam=>(



<FormControlLabel


key={cam.id}


label={cam.name}


control={



<Checkbox


checked={selectedCamera===cam.id}


onChange={()=>setSelectedCamera(cam.id)}


/>


}


/>



))


}




</Grid>









{/* MODELS */}



<Grid item xs={6}>



<Typography fontWeight={800}>

Select AI Models

</Typography>







{


models.map(model=>(



<FormControlLabel


key={model.id}


label={model.name}


control={



<Checkbox


checked={

selectedModels.includes(

model.id

)

}


onChange={()=>toggleModel(model.id)}


/>


}


/>



))


}





</Grid>





</Grid>



</DialogContent>









<DialogActions>





<Button

onClick={()=>setOpen(false)}

>

Cancel

</Button>








<Button

onClick={saveMapping}

sx={orangeBtn}

>

Save

</Button>





</DialogActions>





</Dialog>









</Box>


);



}












// =====================
// STYLES
// =====================


const head={

color:"#94a3b8",

fontWeight:700

};







const cell={

color:"white"

};







const chip={

background:"#2563eb",

color:"white",

mr:1,

mb:1

};







const orangeBtn={


background:"#f97316",

color:"white",

fontWeight:700,


"&:hover":{

background:"#ea580c"

}


};









export default Mapping;