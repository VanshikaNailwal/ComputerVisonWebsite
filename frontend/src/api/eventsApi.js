import api from "./axios";









// =====================================
// GET EVENTS
// Server side pagination
//
// Example:
// /events?page=1&limit=20
// =====================================

export const getEvents = async(

    page = 1,

    limit = 20

)=>{



    const response = await api.get(

        "/events",

        {

            params:{

                page,

                limit

            }

        }

    );





    return response.data;



};












// =====================================
// DELETE EVENT
// =====================================

export const deleteEvent = async(

    id

)=>{



    const response = await api.delete(

        `/events/${id}`

    );




    return response.data;



};












// =====================================
// UPDATE EVENT STATUS
// =====================================

export const updateEventStatus = async(

    id,

    data

)=>{



    const response = await api.patch(

        `/events/${id}/status`,

        data

    );




    return response.data;



};