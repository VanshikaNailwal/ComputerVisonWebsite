import asyncio


import cv2


from concurrent.futures import ThreadPoolExecutor



from app.database import SessionLocal


from app.cameras.models import Camera


from app.ai.manager import (

    start_camera_ai,

    get_ai_status

)









# ----------------------------------
# Settings
# ----------------------------------

CHECK_INTERVAL = 30










# ----------------------------------
# Thread Pool
# ----------------------------------

executor = ThreadPoolExecutor(

    max_workers=10

)











# ----------------------------------
# Check Single Camera
# ----------------------------------

def check_camera_status(

    camera_id,

    rtsp_url

):


    try:



        cap=cv2.VideoCapture(

            rtsp_url,

            cv2.CAP_FFMPEG

        )








        cap.set(

            cv2.CAP_PROP_OPEN_TIMEOUT_MSEC,

            5000

        )



        cap.set(

            cv2.CAP_PROP_READ_TIMEOUT_MSEC,

            5000

        )









        online=False







        for _ in range(3):



            ret,frame=cap.read()





            if ret and frame is not None:



                online=True



                break







        cap.release()








        if online:



            return (

                camera_id,

                "ONLINE"

            )







        return (

            camera_id,

            "OFFLINE"

        )









    except Exception:



        return (

            camera_id,

            "OFFLINE"

        )















# ----------------------------------
# Monitor Cameras
# ----------------------------------

async def camera_monitor():




    print(

        "🔥 Camera Monitor Started"

    )










    while True:




        db=SessionLocal()







        try:




            cameras=db.query(

                Camera

            ).all()










            loop=asyncio.get_running_loop()










            tasks=[




                loop.run_in_executor(

                    executor,


                    check_camera_status,


                    cam.id,


                    cam.rtsp_url

                )



                for cam in cameras



            ]










            results=await asyncio.gather(

                *tasks

            )













            for camera_id,new_status in results:








                camera=db.query(

                    Camera

                ).filter(

                    Camera.id==camera_id

                ).first()







                if not camera:



                    continue










                old_status=camera.connection_status










                # update DB

                camera.connection_status=new_status











                # ----------------------------------
                # Print only when changed
                # ----------------------------------

                if old_status != new_status:




                    print(

                        f"📡 {camera.name}: "

                        f"{old_status} ➜ {new_status}"

                    )












                # ----------------------------------
                # Auto Start AI
                # ----------------------------------

                if new_status=="ONLINE":








                    if len(camera.model_mappings)>0:








                        ai=get_ai_status(

                            camera.id

                        )









                        if not ai["running"]:








                            print(

                                "🚀 Starting AI:",

                                camera.name

                            )








                            start_camera_ai(

                                camera.id

                            )










            db.commit()













        except Exception as e:





            print(

                "❌ Monitor Error:",

                e

            )









        finally:




            db.close()












        await asyncio.sleep(

            CHECK_INTERVAL

        )