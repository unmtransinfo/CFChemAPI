from flask import Flask
import psycopg2
class database:
    def connect(app: Flask):
        return psycopg2.connect(
            host=app.config.get('DB_HOST'),
            database=app.config.get('DB_DATABASE'),
            user=app.config.get('DB_USER'),
            password=app.config.get('DB_PASSWORD'),
            port=app.config.get('DB_PORT')
        )
    
    def select(app: Flask, query: str):
        connection = database.connect(app)

        cursor = connection.cursor()
        try:
            cursor.execute(query)
            res = cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()        
            connection.close()
        return res