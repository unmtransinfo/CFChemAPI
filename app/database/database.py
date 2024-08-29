"""
@author Jack Ringer
Date: 8/28/2024
Description:
Class for operations with Badapple2 (+Badapple comparison) DB.
"""

import psycopg2
import psycopg2.extras
from flask import abort, current_app
from psycopg2 import sql
from rdkit import Chem


class BadappleDB:
    @staticmethod
    def connect():
        return psycopg2.connect(
            host=current_app.config.get("DB_HOST"),
            database=current_app.config.get("DB_DATABASE"),
            user=current_app.config.get("DB_USER"),
            password=current_app.config.get("DB_PASSWORD"),
            port=current_app.config.get("DB_PORT"),
        )

    @staticmethod
    def select(query: sql.SQL):
        connection = BadappleDB.connect()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            cursor.execute(query)
            res = cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            raise error
        finally:
            cursor.close()
            connection.close()
        return res

    def index_compound(cid: int):
        try:
            cid = int(cid)
        except:
            return abort(400, "Invalid cid provided")
        query = sql.SQL("SELECT isosmi from compound where cid={cid} LIMIT 1").format(
            cid=sql.Literal(cid)
        )
        result = BadappleDB.select(query)
        return result

    def search_scaffold(scafsmi: str):
        # first canonicalize SMILES
        try:
            scafsmi = Chem.MolToSmiles(Chem.MolFromSmiles(scafsmi))
        except Exception:
            return abort(400, "Invalid SMILES provided")
        query = sql.SQL(
            "SELECT scafsmi,pscore,prank,in_drug from scaffold where scafsmi={scafsmi} LIMIT 1"
        ).format(scafsmi=sql.Literal(scafsmi))
        result = BadappleDB.select(query)
        return result
