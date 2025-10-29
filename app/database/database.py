import psycopg2
import psycopg2.extras
from flask import abort, current_app, request
from psycopg2 import sql
from psycopg2.extensions import AsIs


class database:
    def connect():
        return psycopg2.connect(
            host=current_app.config.get("DB_HOST"),
            database=current_app.config.get("DB_DATABASE"),
            user=current_app.config.get("DB_USER"),
            password=current_app.config.get("DB_PASSWORD"),
            port=current_app.config.get("DB_PORT"),
        )

    def select(query: sql.SQL, query_vars):
        # NOTE: right now this opens up a DB connection for each query
        # this ok for the current use case, but in future may want to consider
        # moving to a better approach (e.g., as in https://github.com/unmtransinfo/Badapple2-API/blob/main/app/database/badapple.py)
        connection = database.connect()

        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            cursor.execute(query, query_vars)
            res = cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            raise error
        finally:
            cursor.close()
            connection.close()
        return res

    def index(db, mol_id=None):
        where = True
        # Only add a where clause if the mol_id is provided
        if mol_id:
            # Because we're using user input that needs to pass AsIs,
            # We force the input to be an integer here.
            try:
                mol_num = int(mol_id)
            except:
                return abort(400, "Invalid mol_id provided")

            where = "mol_id = %d" % (mol_num)
        # Limit the query size
        limit = request.args.get("limit", type=int) or 10
        offset = request.args.get("offset", type=int) or 0
        # Build the query
        query = """
        SELECT * FROM %(database)s
        WHERE %(where)s
        LIMIT %(limit)s
        OFFSET %(offset)s
        """
        vars = {
            "database": AsIs(db),
            "limit": limit,
            "offset": offset,
            "where": AsIs(where),
        }
        lincsCollection = database.select(query, vars)
        return lincsCollection
