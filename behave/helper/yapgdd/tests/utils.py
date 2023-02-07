import sqlite3
import os
from main import Yapgdd as Base


def dict_factory(cursor, row):
    data = {}
    for index, col in enumerate(cursor.description):
        data[col[0]] = row[index]
    return data


class Yapgdd(Base):
    def get_connection(self, dsn):
        return sqlite3.connect(dsn)

    def get_dict_cursor(self, connection):
        connection.row_factory = dict_factory
        return connection.cursor()

    def get_tables(self, cursor):
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [table[0] for table in cursor]


class TestDatabases:
    @classmethod
    def setUpClass(cls):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

        cls.source_db = "/tmp/yapdd.source.db"
        cls.target_db = "/tmp/yapdd.target.db"
        cls.cleanup_test_dbs()

        source_cursor = sqlite3.connect(cls.source_db).cursor()
        target_cursor = sqlite3.connect(cls.target_db).cursor()
        with open(f"{path}/schema.sql") as fh:
            schema = fh.read()
            source_cursor.executescript(schema)
            target_cursor.executescript(schema)

        with open(f"{path}/source.sql") as fh:
            sql = fh.read()
            source_cursor.executescript(sql)

        with open(f"{path}/target.sql") as fh:
            sql = fh.read()
            target_cursor.executescript(sql)

        super(TestDatabases, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.cleanup_test_dbs()

    @classmethod
    def cleanup_test_dbs(cls):
        if os.path.exists(cls.source_db):
            os.remove(cls.source_db)
        if os.path.exists(cls.target_db):
            os.remove(cls.target_db)
