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
    TextField,
    IconButton

} from "@mui/material";



import {

    Add,
    Delete,
    UploadFile

} from "@mui/icons-material";



import api from "../api/axios";


import { useAuth } from "../context/AuthContext";









function Models(){



const {user}=useAuth();




// ===============================
// PERMISSION CHECK
// ===============================

const canManageModels =

user?.is_super_admin

||

user?.permissions?.includes(

"manage_models"

);











const [models,setModels] = useState([]);


const [open,setOpen] = useState(false);


const [error,setError] = useState("");


const [loading,setLoading] = useState(false);






const [form,setForm] = useState({

name:"",

usecase:"",

version:"",

file:null

});












// ----------------------------------
// Load Models
// ----------------------------------

const loadModels = async()=>{


try{


const res = await api.get(

"/models"

);



setModels(

res.data

);



}

catch(err){


console.log(err);


}


};










useEffect(()=>{


loadModels();


},[]);











// ----------------------------------
// Upload Model
// ----------------------------------

const uploadModel = async()=>{



if(!canManageModels)

return;






try{


setError("");


setLoading(true);






if(!form.name.trim()){


setError("Model name required");


setLoading(false);


return;


}





if(!form.usecase.trim()){


setError("Usecase required");


setLoading(false);


return;


}






if(!form.version.trim()){


setError("Version required");


setLoading(false);


return;


}







if(!form.file){


setError("Select model file");


setLoading(false);


return;


}









const data = new FormData();




data.append(

"name",

form.name

);



data.append(

"usecase",

form.usecase

);



data.append(

"version",

form.version

);



data.append(

"file",

form.file

);










await api.post(

"/models/upload",

data,

{

headers:{

"Content-Type":"multipart/form-data"

}

}

);










setOpen(false);




setForm({

name:"",

usecase:"",

version:"",

file:null

});







loadModels();




}

catch(err){



const detail = err.response?.data?.detail;




if(Array.isArray(detail)){


setError(

detail[0]?.msg || "Upload failed"

);


}

else{


setError(

detail || "Upload failed"

);


}



}

finally{


setLoading(false);


}



};











// ----------------------------------
// Delete Model
// ----------------------------------

const deleteModel = async(id)=>{



if(!canManageModels)

return;





const confirmDelete=window.confirm(

"Delete this AI model?"

);



if(!confirmDelete)

return;






try{


await api.delete(

`/models/${id}`

);




loadModels();



}

catch(err){


console.log(err);


}



};











// ----------------------------------
// Status Color
// ----------------------------------

const statusColor=(status)=>{



if(status==="READY"){

return "#16a34a";

}



if(status==="FAILED"){

return "#dc2626";

}



return "#f97316";



};












return (

<Box

sx={{

p:3,

minHeight:"100vh",

background:"#0f172a",

color:"white"

}}

>











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

AI Model Management

</Typography>





<Typography color="#94a3b8">

Upload and monitor AI models

</Typography>




</Box>









{


canManageModels &&


<Button

startIcon={<Add/>}

onClick={()=>setOpen(true)}

sx={orangeBtn}

>

Upload Model

</Button>


}




</Box>














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

"Model",

"Usecase",

"Version",

"File",

"Status",

...(canManageModels?["Actions"]:[])

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


models.map(model=>(



<TableRow key={model.id}>



<TableCell sx={cell}>

{model.name}

</TableCell>






<TableCell sx={cell}>

{model.usecase}

</TableCell>






<TableCell sx={cell}>

v{model.version}

</TableCell>







<TableCell sx={cell}>

{model.filename}

</TableCell>








<TableCell>



<Chip

label={model.status}

sx={{

background:statusColor(model.status),

color:"white"

}}

/>



</TableCell>











{


canManageModels &&


<TableCell>



<IconButton

onClick={()=>deleteModel(model.id)}

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













{/* UPLOAD MODEL */}



<Dialog

open={open}

onClose={()=>setOpen(false)}

PaperProps={{

sx:{

background:"#111827",

color:"white",

width:500

}

}}

>



<DialogTitle>

Upload AI Model

</DialogTitle>








<DialogContent>






<TextField

fullWidth

margin="dense"

label="Model Name"

value={form.name}

sx={input}

onChange={(e)=>

setForm({

...form,

name:e.target.value

})

}

/>








<TextField

fullWidth

margin="dense"

label="Usecase"

value={form.usecase}

sx={input}

onChange={(e)=>

setForm({

...form,

usecase:e.target.value

})

}

/>








<TextField

fullWidth

margin="dense"

label="Version"

value={form.version}

sx={input}

onChange={(e)=>

setForm({

...form,

version:e.target.value

})

}

/>











<Button

component="label"

startIcon={<UploadFile/>}

sx={{

mt:2,

color:"#38bdf8"

}}

>

Select Model File



<input

hidden

type="file"

accept=".pt"

onChange={(e)=>

setForm({

...form,

file:e.target.files[0]

})

}

/>



</Button>









{

form.file &&


<Typography>

{form.file.name}

</Typography>


}








{

error &&


<Typography color="error">

{error}

</Typography>


}




</DialogContent>









<DialogActions>



<Button

onClick={()=>setOpen(false)}

>

Cancel

</Button>





<Button

disabled={loading}

onClick={uploadModel}

sx={orangeBtn}

>

{

loading

?

"Checking..."

:

"Upload"

}

</Button>



</DialogActions>



</Dialog>








</Box>

);


}












// ===============================
// STYLES
// ===============================


const head={

color:"#94a3b8",

fontWeight:700,

borderColor:"#1f2937"

};






const cell={

color:"white",

borderColor:"#1f2937"

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







export default Models;