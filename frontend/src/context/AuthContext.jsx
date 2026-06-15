import {

    createContext,

    useContext,

    useEffect,

    useState

} from "react";



import api from "../api/axios";







// Create authentication context

const AuthContext = createContext(null);









export const AuthProvider = ({ children }) => {




    // Logged in user data

    const [user, setUser] = useState(null);




    // Loading while checking token

    const [loading, setLoading] = useState(true);










    /*
        Restore login after refresh

        Browser refresh clears React state

        so we call:

        GET /auth/me

    */


    useEffect(() => {


        const checkLogin = async () => {


            const token = localStorage.getItem(

                "token"

            );





            if (!token) {


                setLoading(false);


                return;

            }







            try {


                const response = await api.get(

                    "/auth/me"

                );





                setUser(

                    response.data

                );




            }


            catch (error) {



                localStorage.removeItem(

                    "token"

                );



                localStorage.removeItem(

                    "user"

                );



                setUser(null);



            }



            finally {


                setLoading(false);

            }


        };






        checkLogin();



    }, []);











    /*
        LOGIN FUNCTION

        Calls FastAPI:

        POST /auth/login

    */


    const login = async (

        email,

        password

    ) => {




        const response = await api.post(

            "/auth/login",


            {


                email,


                password


            }


        );






        // Save JWT

        localStorage.setItem(

            "token",


            response.data.token

        );







        // Save user

        localStorage.setItem(

            "user",


            JSON.stringify(

                response.data.user

            )

        );







        setUser(

            response.data.user

        );







        return response.data;


    };











    /*
        LOGOUT FUNCTION
    */


    const logout = () => {




        localStorage.removeItem(

            "token"

        );



        localStorage.removeItem(

            "user"

        );





        setUser(null);



    };












    return (



        <AuthContext.Provider


            value={{


                user,


                login,


                logout,


                loading


            }}


        >



            {children}




        </AuthContext.Provider>


    );


};









export const useAuth = () => {


    return useContext(

        AuthContext

    );


};