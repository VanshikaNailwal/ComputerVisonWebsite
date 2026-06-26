import os
import sys

from pathlib import Path

import psycopg2

from psycopg2.extensions import (
    ISOLATION_LEVEL_AUTOCOMMIT
)

from alembic.config import Config
from alembic import command



# ----------------------------------
# Detect Base Directory
# ----------------------------------

if getattr(sys, "frozen", False):

    BASE_DIR = Path(
        sys._MEIPASS
    )

    RESOURCE_DIR = BASE_DIR


elif os.getenv("HMEL_BASE_DIR"):

    BASE_DIR = Path(
        os.getenv("HMEL_BASE_DIR")
    )

    RESOURCE_DIR = BASE_DIR


else:

    BASE_DIR = (
        Path(__file__)
        .resolve()
        .parents[1]
    )

    RESOURCE_DIR = BASE_DIR





# ----------------------------------
# DATABASE CONFIG
# ----------------------------------

DB_NAME = "hmel_cv"


DB_USER = "postgres"


POSTGRES_PASSWORD = "14232517"


POSTGRES_HOST = "localhost"


POSTGRES_PORT = 5432





# ----------------------------------
# Setup Database
# ----------------------------------

def setup_database():


    print(
        "🚀 Setting up VisionX database..."
    )


    conn = psycopg2.connect(

        dbname="postgres",

        user=DB_USER,

        password=POSTGRES_PASSWORD,

        host=POSTGRES_HOST,

        port=POSTGRES_PORT

    )


    conn.set_isolation_level(
        ISOLATION_LEVEL_AUTOCOMMIT
    )


    cursor = conn.cursor()




    # ------------------------------
    # Create Database
    # ------------------------------

    cursor.execute(

        f"""
        SELECT 1
        FROM pg_database
        WHERE datname='{DB_NAME}';
        """

    )


    exists = cursor.fetchone()




    if not exists:


        cursor.execute(

            f"""
            CREATE DATABASE {DB_NAME};
            """

        )


        print(
            "✅ Database created"
        )


    else:


        print(
            "ℹ️ Database already exists"
        )




    cursor.close()

    conn.close()





    # ------------------------------
    # Run Alembic
    # ------------------------------

    os.environ[
        "HMEL_BASE_DIR"
    ] = str(
        BASE_DIR
    )



    alembic_ini = (

        RESOURCE_DIR
        /
        "alembic.ini"

    )



    migration_path = (

        RESOURCE_DIR
        /
        "migrations"

    )



    print(
        f"📂 Alembic: {alembic_ini}"
    )


    print(
        f"📂 Migrations: {migration_path}"
    )




    if not alembic_ini.exists():


        raise Exception(

            f"Alembic config missing: {alembic_ini}"

        )




    if not migration_path.exists():


        raise Exception(

            f"Migration folder missing: {migration_path}"

        )




    alembic_cfg = Config(

        str(alembic_ini)

    )




    alembic_cfg.set_main_option(

        "script_location",

        str(migration_path)

    )




    command.upgrade(

        alembic_cfg,

        "head"

    )




    print(
        "🎉 VisionX database setup completed"
    )





if __name__ == "__main__":


    setup_database()