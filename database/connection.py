import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Va+Das-Ef333",
        database="electronics_db"
    )