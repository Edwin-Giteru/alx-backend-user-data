#!/usr/bin/env python3
import re
import logging
from typing import List
import os
import mysql.connector


PII_FIELDS = ("name", "email", "ssn", "phone", "password")

def filter_datum(fields, redaction, message, separator):
    return re.sub(r'({})=[^{}]*'.format('|'.join(fields), separator), lambda m: m.group().split('=')[0] + '=' + redaction, message)

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)
    
def get_logger() -> logging.Logger:
        
        logger= logging.getLogger("user_data")
        logger.setLevel(logging.INFO)
        logger.propagate = False
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
        logger.addHandler(stream_handler)

        return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
     
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "root1")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connection.MySQLConnection(
         user = username,
         password = password,
         host = host,
         database = db_name
    )
    return connection

def main():
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [i[0] for i in cursor.description]
    
    for row in cursor.fetchall():
        message = "{}".format(
            "; ".join("{}={}".format(k, v) for k, v in zip(field_names, row))
        )
        logger.info(message)
    
    cursor.close()
    db.close()
 

if __name__ == "__main__":
     main()