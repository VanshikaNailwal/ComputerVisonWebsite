import os
import sys
import secrets
import string
from pathlib import Path

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from alembic.config import Config
from alembic import command


# ----------------------------------
# Detect Base Directory
# Normal Python + PyInstaller EXE
# ----------------------------------

if getattr(sys, "frozen", False):

    # PyInstaller:
    # dist/HMELVision/_internal
    BASE_DIR = Path(sys._MEIPASS)


elif os.getenv("HMEL_BASE_DIR"):

    BASE_DIR = Path(
        os.getenv("HMEL_BASE_DIR")
    )


else:

    BASE_DIR = Path(
        __file__
    ).resolve().parents[1]




# ----------------------------------
# CONFIG
# ----------------------------------

DB_NAME = "hmel_cv"

DB_USER = "hmel_service"


POSTGRES_ADMIN = "postgres"

POSTGRES_PASSWORD = "14232517"

POSTGRES_HOST = "localhost"

POSTGRES_PORT = 5432



ENV_FILE = BASE_DIR / ".env"




# ----------------------------------
# Generate Password
# ----------------------------------

def generate_password():

    chars = (
        string.ascii_letters
        +
        string.digits
    )

    return "".join(
        secrets.choice(chars)
        for _ in range(24)
    )






# ----------------------------------
# Setup Database
# ----------------------------------

def setup_database():

    print(
        "🚀 Setting up HMEL database..."
    )


    db_password = generate_password()



    # ----------------------------------
    # Connect postgres admin
    # ----------------------------------

    conn = psycopg2.connect(
        dbname="postgres",
        user=POSTGRES_ADMIN,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )


    conn.set_isolation_level(
        ISOLATION_LEVEL_AUTOCOMMIT
    )


    cursor = conn.cursor()




    # ----------------------------------
    # Create / update service user
    # ----------------------------------

    cursor.execute(
        f"""
        DO $$

        BEGIN

            IF NOT EXISTS (

                SELECT FROM pg_catalog.pg_roles

                WHERE rolname='{DB_USER}'

            )

            THEN

                CREATE ROLE {DB_USER}
                LOGIN PASSWORD '{db_password}';


            ELSE


                ALTER ROLE {DB_USER}
                WITH PASSWORD '{db_password}';


            END IF;

        END

        $$;
        """
    )


    print(
        "✅ Database user configured"
    )






    # ----------------------------------
    # Check database
    # ----------------------------------

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
            CREATE DATABASE {DB_NAME}

            OWNER {DB_USER};
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







    # ----------------------------------
    # Generate .env
    # ----------------------------------

    database_url = (
        f"postgresql://{DB_USER}:{db_password}"
        f"@localhost:5432/{DB_NAME}"
    )


    ENV_FILE.write_text(
f"""
# ==================================
# AUTO GENERATED CONFIG
# ==================================

DATABASE_URL={database_url}

SECRET_KEY={secrets.token_hex(32)}

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60


APP_NAME=HMEL Vision Platform

ENVIRONMENT=production


STORAGE_PATH=storage

MODEL_PATH=storage/models

EVIDENCE_PATH=storage/evidence


CONFIDENCE_THRESHOLD=0.4

FRAME_SKIP=5

ALERT_COOLDOWN=20

"""
    )


    print(
        "✅ Production .env generated"
    )








    # ----------------------------------
    # Run Alembic
    # ----------------------------------

    os.environ["HMEL_BASE_DIR"] = str(BASE_DIR)


    alembic_ini = (
        BASE_DIR
        /
        "alembic.ini"
    )


    migration_path = (
        BASE_DIR
        /
        "migrations"
    )



    print(
        f"📂 Alembic config: {alembic_ini}"
    )


    print(
        f"📂 Migration folder: {migration_path}"
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
        "🎉 HMEL database setup completed"
    )





if __name__ == "__main__":

    setup_database()