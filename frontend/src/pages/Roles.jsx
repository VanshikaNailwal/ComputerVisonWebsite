import {

    useEffect,

    useState

} from "react";



import {

    Box,
    Typography,
    Paper,
    Button,
    TextField,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Table,
    TableHead,
    TableRow,
    TableCell,
    TableBody,
    Checkbox,
    FormControlLabel,
    Chip,
    IconButton

} from "@mui/material";



import {

    Add,
    Edit,
    Delete

} from "@mui/icons-material";



import api from "../api/axios";


import { useAuth } from "../context/AuthContext";









function Roles() {



    const { user } = useAuth();



    const [roles, setRoles] = useState([]);


    const [permissions, setPermissions] = useState([]);



    const [open, setOpen] = useState(false);



    const [editId, setEditId] = useState(null);





    const [form, setForm] = useState({


        name: "",


        description: "",


        permissions: []


    });









    // =========================
    // PERMISSION CHECK
    // =========================

    const canManage = () => {



        if (user?.is_super_admin) {


            return true;


        }



        return user?.permissions?.includes(

            "manage_roles"

        );



    };









    // =========================
    // LOAD DATA
    // =========================

    const loadData = () => {



        api.get(

            "/roles"

        )

            .then(res => {


                setRoles(res.data);


            });






        api.get(

            "/permissions"

        )

            .then(res => {


                setPermissions(res.data);


            });



    };











    useEffect(() => {


        loadData();


    }, []);











    // =========================
    // PERMISSION TOGGLE
    // =========================

    const togglePermission = (name) => {



        let selected = [...form.permissions];




        if (selected.includes(name)) {



            selected = selected.filter(

                p => p !== name

            );


        }


        else {


            selected.push(name);


        }






        setForm({


            ...form,


            permissions: selected


        });



    };











    // =========================
    // OPEN EDIT
    // =========================

    const openEdit = (role) => {



        setEditId(role.id);



        setForm({


            name: role.name,


            description: role.description || "",


            permissions: role.permissions || []


        });



        setOpen(true);



    };











    // =========================
    // SAVE ROLE
    // =========================

    const saveRole = async () => {





        if (editId) {



            await api.patch(


                `/roles/${editId}`,


                form


            );



        }





        else {



            await api.post(


                "/roles",


                form


            );



        }








        setOpen(false);


        setEditId(null);



        setForm({


            name: "",

            description: "",

            permissions: []


        });




        loadData();



    };











    // =========================
    // DELETE ROLE
    // =========================

    const deleteRole = async (id) => {



        const ok = window.confirm(

            "Delete this role?"

        );




        if (!ok) {


            return;


        }






        await api.delete(


            `/roles/${id}`


        );





        loadData();



    };









    return (

        <Box

            sx={{


                p: 3,


                background: "#0f172a",


                minHeight: "100vh",


                color: "white"


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

                        Role Management

                    </Typography>



                    <Typography color="#94a3b8">

                        Create roles and assign permissions

                    </Typography>



                </Box>








                {

                    canManage()

                    &&


                    <Button

                        startIcon={<Add />}

                        onClick={() => setOpen(true)}

                        sx={{

                            background: "#f97316",

                            color: "white",

                            fontWeight: 800

                        }}

                    >

                        Create Role

                    </Button>


                }



            </Box>










            <Paper

                sx={{

                    background: "#111827",

                    border: "1px solid #334155",

                    borderRadius: 3,

                    overflow: "hidden"

                }}

            >


                <Table>


                    <TableHead>


                        <TableRow>


                            <TableCell sx={head}>Role</TableCell>

                            <TableCell sx={head}>Description</TableCell>

                            <TableCell sx={head}>Permissions</TableCell>


                            {


                                canManage()

                                &&

                                <TableCell sx={head}>Action</TableCell>


                            }



                        </TableRow>


                    </TableHead>








                    <TableBody>



                        {


                            roles.map(role => (



                                <TableRow key={role.id}>



                                    <TableCell sx={cell}>

                                        {role.name}

                                    </TableCell>





                                    <TableCell sx={cell}>

                                        {role.description || "-"}

                                    </TableCell>







                                    <TableCell sx={cell}>


                                        {


                                            role.permissions?.map(p => (


                                                <Chip

                                                    key={p}

                                                    label={p}

                                                    sx={{

                                                        m: .5,

                                                        background: "#334155",

                                                        color: "white"

                                                    }}

                                                />


                                            ))


                                        }



                                    </TableCell>









                                    {

                                        canManage()

                                        &&


                                        <TableCell sx={cell}>



                                            <IconButton

                                                onClick={() => openEdit(role)}

                                                sx={{ color: "#38bdf8" }}

                                            >

                                                <Edit />

                                            </IconButton>





                                            <IconButton

                                                onClick={() => deleteRole(role.id)}

                                                sx={{ color: "#ef4444" }}

                                            >

                                                <Delete />

                                            </IconButton>




                                        </TableCell>


                                    }







                                </TableRow>


                            ))


                        }




                    </TableBody>


                </Table>


            </Paper>













            {/* DIALOG */}


            <Dialog

                open={open}

                onClose={() => setOpen(false)}

                PaperProps={{

                    sx: {

                        background: "#111827",

                        color: "white",

                        width: 550

                    }

                }}

            >






                <DialogTitle>

                    {

                        editId

                            ?

                            "Edit Role"

                            :

                            "Create Role"

                    }

                </DialogTitle>







                <DialogContent>




                    <TextField

                        fullWidth

                        label="Role"

                        margin="normal"

                        value={form.name}

                        sx={field}

                        onChange={(e) =>

                            setForm({

                                ...form,

                                name: e.target.value.toUpperCase()

                            })

                        }

                    />






                    <TextField

                        fullWidth

                        label="Description"

                        margin="normal"

                        value={form.description}

                        sx={field}

                        onChange={(e) =>

                            setForm({

                                ...form,

                                description: e.target.value

                            })

                        }

                    />







                    <Typography mt={2}>

                        Permissions

                    </Typography>






                    {


                        permissions.map(p => (



                            <FormControlLabel


                                key={p.id}


                                label={p.name}


                                control={


                                    <Checkbox

                                        checked={

                                            form.permissions.includes(p.name)

                                        }

                                        onChange={() => togglePermission(p.name)}

                                    />


                                }


                            />


                        ))


                    }




                </DialogContent>








                <DialogActions>


                    <Button

                        onClick={() => setOpen(false)}

                    >

                        Cancel

                    </Button>




                    <Button

                        onClick={saveRole}

                        sx={{

                            background: "#f97316",

                            color: "white"

                        }}

                    >

                        Save

                    </Button>


                </DialogActions>




            </Dialog>







        </Box>

    );


}









const head = {

    color: "#94a3b8",

    fontWeight: 800,

    borderColor: "#334155"

};




const cell = {

    color: "white",

    borderColor: "#334155"

};




const field = {


    "& input": {

        color: "white"

    },


    "& label": {

        color: "#94a3b8"

    },


    "& fieldset": {

        borderColor: "#334155"

    }


};








export default Roles;