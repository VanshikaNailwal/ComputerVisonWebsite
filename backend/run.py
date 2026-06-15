import time

import socket

import threading

import webbrowser

import sys

import os

from pathlib import Path



import uvicorn







# ----------------------------------
# Detect Running Mode
# Normal Python / PyInstaller EXE
# ----------------------------------

if getattr(

    sys,

    "frozen",

    False

):


    BASE_DIR = Path(

        sys.executable

    ).resolve().parent



else:


    BASE_DIR = Path(

        __file__

    ).resolve().parent







# ----------------------------------
# Share BASE_DIR with all modules
# (Needed for PyInstaller)
# ----------------------------------

os.environ[

    "HMEL_BASE_DIR"

] = str(

    BASE_DIR

)










# ----------------------------------
# Paths
# ----------------------------------

ENV_FILE = (

    BASE_DIR

    /

    ".env"

)










# ----------------------------------
# Wait until backend starts
# ----------------------------------

def wait_for_server():



    while True:



        try:



            sock = socket.socket()



            sock.connect(

                (

                    "127.0.0.1",

                    8000

                )

            )



            sock.close()



            return





        except Exception:



            time.sleep(

                1

            )












# ----------------------------------
# Open Browser
# ----------------------------------

def open_browser():



    wait_for_server()



    webbrowser.open(

        "http://127.0.0.1:8000"

    )













# ----------------------------------
# Setup Database
# First installation only
# ----------------------------------

def initialize_database():



    if not ENV_FILE.exists():



        print(

            "First startup detected"

        )





        from scripts.setup_database import setup_database





        setup_database()






    else:



        print(

            "Database already configured"

        )













# ----------------------------------
# Start Application
# ----------------------------------

if __name__=="__main__":







    initialize_database()









    threading.Thread(

        target=open_browser,


        daemon=True

    ).start()










    uvicorn.run(

        "app.main:app",


        host="127.0.0.1",


        port=8000,


        reload=False

    )