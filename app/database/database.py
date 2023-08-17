from flask import Flask, request, abort
from flask import current_app
import psycopg2
import psycopg2.extras
from psycopg2.extensions import AsIs

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

        cursor = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
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

    def index(db, mol_id = None, searchable = []):
        whereColumn = []
        whereValue = []
        # Only add a where clause if the mol_id is provided
        if mol_id:
            # Because we're using user input that needs to pass AsIs,
            # We force the input to be an integer here.
            try:
                mol_num = int(mol_id)
            except:
                return abort(400, 'Invalid mol_id provided')

            whereColumn += 'mol_id = ' 
            whereValue  += mol_num
        for search in searchable:
            if request.args.get(search):
                whereColumn += '`' + search + '` = '
                whereValue  += '' + request.args.get(search)
        # Limit the query size
        limit = request.args.get('limit', type=int) or 10
        offset = request.args.get('offset', type=int) or 0
        # Build the query
        # TODO: ensure where searchables are properly escaped
        # if whereColumn.count() == 0:
        #     where = True
        # else:
        #     for i in range(whereColumn.count()):
        #         where += ' ' + whereColumn + whereValue + ' '
        #         if i > 0:
        #             where += ' AND '
        lincsCollection = database.select("""
        SELECT * FROM %(database)s
        WHERE %(where)s
        LIMIT %(limit)s
        OFFSET %(offset)s
        """, {'database': AsIs(db), 'limit': limit, 'offset': offset, 'where':where})
        return lincsCollection