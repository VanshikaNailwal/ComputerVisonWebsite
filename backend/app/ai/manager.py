from threading import (
    Thread,
    Lock
)


from app.ai.stream import process_camera










# ----------------------------------
# Active AI Workers
# camera_id -> Thread
# ----------------------------------

running_cameras = {}








# ----------------------------------
# Stop Signals
# camera_id -> bool
# ----------------------------------

stop_flags = {}









# ----------------------------------
# Thread Safety Lock
# ----------------------------------

manager_lock = Lock()












# ----------------------------------
# Start AI Process
# ----------------------------------

def start_ai_process(

    camera_id

):


    camera_key = str(

        camera_id

    )







    with manager_lock:





        # ----------------------------------
        # Check Existing Thread
        # ----------------------------------

        thread = running_cameras.get(

            camera_key

        )







        if thread and thread.is_alive():




            return {

                "status":"already_running"

            }










        # cleanup old dead thread

        running_cameras.pop(

            camera_key,

            None

        )



        stop_flags.pop(

            camera_key,

            None

        )









        # reset stop signal

        stop_flags[

            camera_key

        ] = False










        print(

            "🚀 Starting AI Worker:",

            camera_id

        )










        thread = Thread(

            target=process_camera,


            args=(

                camera_id,

                stop_flags

            ),


            daemon=True,


            name=f"AI-{camera_key}"

        )









        thread.start()










        running_cameras[

            camera_key

        ] = thread










        return {

            "status":"started"

        }

















# ----------------------------------
# Stop AI Process
# ----------------------------------

def stop_ai_process(

    camera_id

):



    camera_key = str(

        camera_id

    )








    with manager_lock:







        thread = running_cameras.get(

            camera_key

        )








        if not thread:




            return {

                "status":"not_running"

            }











        stop_flags[

            camera_key

        ] = True










        print(

            "🛑 Stop requested:",

            camera_id

        )









        return {

            "status":"stopping"

        }

















# ----------------------------------
# Get AI Status
# ----------------------------------

def get_ai_status(

    camera_id

):



    camera_key=str(

        camera_id

    )







    with manager_lock:






        thread = running_cameras.get(

            camera_key

        )








        if not thread:




            return {

                "running":False

            }









        alive = thread.is_alive()










        # cleanup finished workers

        if not alive:




            running_cameras.pop(

                camera_key,

                None

            )



            stop_flags.pop(

                camera_key,

                None

            )











        return {

            "running":alive

        }















# ----------------------------------
# Called By Camera Monitor
# ----------------------------------

def start_camera_ai(

    camera_id

):


    return start_ai_process(

        camera_id

    )