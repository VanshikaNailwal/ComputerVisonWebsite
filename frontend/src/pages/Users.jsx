import {

    useEffect,

    useState

} from "react";



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

    IconButton

} from "@mui/material";



import {

    Delete,
    Security

} from "@mui/icons-material";



import api from "../api/axios";


import { useAuth } from "../context/AuthContext";











function Users(){



const {user:currentUser}=useAuth();



const [users,setUsers]=useState([]);


const [pending,setPending]=useState([]);









const hasPermission=(permission)=>{


if(currentUser?.is_super_admin){


return true;


}



return currentUser?.permissions?.includes(

permission

);


};









const loadUsers=()=>{



api.get(

"/users"

)

.then(res=>{

setUsers(res.data);

});







api.get(

"/users/pending"

)

.then(res=>{

setPending(res.data);

});


};











useEffect(()=>{


loadUsers();


},[]);















const approve=async(id)=>{



await api.patch(

`/users/${id}/approve`

);



loadUsers();



};












const reject=async(id)=>{



await api.patch(

`/users/${id}/reject`

);



loadUsers();



};












const deleteUser=async(selectedUser)=>{



if(selectedUser.is_super_admin){


alert(

"Super admin cannot be deleted"

);


return;


}








const confirmDelete=window.confirm(

"Are you sure you want to remove this user?"

);




if(!confirmDelete){

return;

}








await api.delete(

`/users/${selectedUser.id}`

);







loadUsers();



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










<Typography

variant="h4"

fontWeight={900}

>

User Management

</Typography>







<Typography

color="#94a3b8"

mb={4}

>

Approve users and manage access

</Typography>











{/* Pending Requests */}



<Typography

variant="h5"

fontWeight={800}

mb={2}

>

Pending Requests

</Typography>










{

pending.length===0 &&


<Typography color="#94a3b8">

No pending requests

</Typography>


}











{


pending.map(user=>(



<Paper


key={user.id}


sx={{

background:"#111827",

border:"1px solid #334155",

borderRadius:3,

p:3,

mb:2,

color:"white"

}}

>





<Typography

fontSize={20}

fontWeight={800}

>

{user.name}

</Typography>






<Typography color="#94a3b8">

{user.email}

</Typography>





<Typography mt={1}>

Department : {user.department}

</Typography>





<Typography>

Requested Role : {user.role}

</Typography>









{

hasPermission("manage_users") &&


<Box mt={2}>



<Button


onClick={()=>approve(user.id)}


sx={{

background:"#16a34a",

color:"white",

mr:2

}}

>

Approve

</Button>







<Button


onClick={()=>reject(user.id)}


sx={{

background:"#dc2626",

color:"white"

}}

>

Reject

</Button>




</Box>


}




</Paper>


))


}














{/* ALL USERS */}



<Typography

variant="h5"

fontWeight={800}

mt={5}

mb={2}

>

All Users

</Typography>










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

"Email",

"Role",

"Status",

"Type",

"Action"

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


users.map(user=>(



<TableRow key={user.id}>



<TableCell sx={cell}>

{user.name}

</TableCell>






<TableCell sx={cell}>

{user.email}

</TableCell>







<TableCell sx={cell}>

{user.role}

</TableCell>








<TableCell sx={cell}>


<Chip

label={user.status}

sx={{

color:"white",

background:

user.status==="ACTIVE"

?

"#16a34a"

:

user.status==="PENDING"

?

"#eab308"

:

"#dc2626"

}}

/>


</TableCell>









<TableCell sx={cell}>


{


user.is_super_admin

?


<Chip

icon={<Security/>}

label="SUPER ADMIN"

sx={{

background:"#f97316",

color:"white",

fontWeight:800,

"& svg":{

color:"white"

}

}}

/>


:


"-"


}



</TableCell>











<TableCell sx={cell}>


{


hasPermission("manage_users")

&&

!user.is_super_admin

&&


<IconButton


onClick={()=>deleteUser(user)}


sx={{

color:"#ef4444"

}}

>


<Delete />


</IconButton>


}



</TableCell>








</TableRow>


))


}





</TableBody>



</Table>



</Paper>







</Box>

);

}










const head={

color:"#94a3b8",

fontWeight:700,

borderColor:"#1f2937"

};







const cell={

color:"white",

borderColor:"#1f2937"

};








export default Users;