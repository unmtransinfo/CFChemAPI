from flask import Flask
from flask import current_app
import psycopg2
class database:
    def connect():
        return psycopg2.connect(
            host=current_app.config.get('DB_HOST'),
            database=current_app.config.get('DB_DATABASE'),
            user=current_app.config.get('DB_USER'),
            password=current_app.config.get('DB_PASSWORD'),
            port=current_app.config.get('DB_PORT')
        )
    
    def select(query: str, vars):
        connection = database.connect()

        cursor = connection.cursor()
        try:
            cursor.execute(query, vars)
            res = cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            raise error
        finally:
            cursor.close()        
            connection.close()
        return res