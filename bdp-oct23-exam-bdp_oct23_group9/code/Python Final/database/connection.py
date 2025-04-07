from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv('DATABASE_USER')
PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_Name')

if not USERNAME or not PASSWORD:
    raise ValueError("Missing DATABASE_USER or DATABASE_PASSWORD environment variables")

HOST = 'localhost'
PORT = '5432'
DB_URL = f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"

engine = create_engine(DB_URL)

def save_to_database(data, table_name="processed_data"):
    data.to_sql(table_name, engine, if_exists='replace', index=False)
    print("Data has been saved in the database.")


#check if this is connected to database or not 

# def check_database_connection():
#     try:
#         with engine.connect():
#             print("Successfully connected to the database.")
#     except Exception as e:
#         print(f"Failed to connect to the database: {str(e)}")

# check_database_connection()
