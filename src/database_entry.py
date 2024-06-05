import psycopg2
from utils import config
from datetime import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def connect():
    try:
        with psycopg2.connect(
            host = config['DATABASE']['HOST'],
            database = config['DATABASE']['DB'],
            user = config['DATABASE']['USER'],
            password = config['DATABASE']['PASSWORD']
        ) as conn:
            logger.info('Connected to PostgreSQL server')
            return conn
    except(psycopg2.DatabaseError, Exception) as error:
        logger.error(error)

def write_results_to_database(filename, results_dir):
    conn = connect()
    cursor = conn.cursor()
    timestamp = datetime.now()
    try:
        cursor.execute("""INSERT INTO inference (filename, model, start_at, results_file) VALUES (%s, %s, %s, %s)""",
                       (filename, config['INFERENCE_MODEL'], timestamp, results_dir))
        conn.commit()
        logger.info('Insert operation successful')
    except psycopg2.Error:
        conn.rollback()
        logger.error('error inserting into inference table')
    finally:
        logger.info('Closing database connection')
        cursor.close()
        conn.close()

