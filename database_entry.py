import psycopg2
from utils import config
from datetime import datetime

def connect():
    try:
        with psycopg2.connect(
            host = config['DATABASE']['HOST'],
            database = config['DATABASE']['DB'],
            user = config['DATABASE']['USER'],
            password = config['DATABASE']['PASSWORD']
        ) as conn:
            print('Connected to PostgreSQL server')
            return conn
    except(psycopg2.DatabaseError, Exception) as error:
        print(error)

def write_results_to_database(filename, results):
    conn = connect()
    cursor = conn.cursor()
    timestamp = datetime.now()
    try:
        cursor.execute("""INSERT INTO inference (filename, model, start_at) VALUES (%s, %s, %s)""",
                       (filename, config['INFERENCE_MODEL'], timestamp))
        conn.commit()
    except psycopg2.Error:
        conn.rollback()
        print('error inserting into inference table')
    finally:
        cursor.close()
        conn.close()

