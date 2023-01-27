import os
import psycopg2
import psycopg2.extras
from urllib.parse import urlparse
from tabulate import tabulate


class Yapgdd:
    def __init__(
        self,
        source_dsn,
        target_dsn,
        exclude_columns=[],
        exclude_tables=[],
        output_dir="/tmp",
    ):
        self.source_conn = self.get_connection(source_dsn)
        self.target_conn = self.get_connection(target_dsn)
        self.source_cursor = self.source_conn.cursor()
        self.target_cursor = self.target_conn.cursor()
        self.exclude_columns = set(exclude_columns)
        self.exclude_tables = exclude_tables
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        self.source_tables = self.get_tables(self.source_cursor)
        self.target_tables = self.get_tables(self.target_cursor)
        pass

    def get_connection(self, dsn):
        url = urlparse(dsn)
        connection_details = {
            "dbname": url.path.replace("/", ""),
            "user": url.username,
            "password": url.password,
            "port": url.port,
            "host": url.hostname,
        }
        return psycopg2.connect(**connection_details)

    def get_dict_cursor(self, connection):
        return connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def get_tables(self, cursor):
        cursor.execute(
            """SELECT table_name FROM information_schema.tables
               WHERE table_schema = 'public'"""
        )
        return [table[0] for table in cursor.fetchall()]

    def get_columns(self, cursor, table):
        cursor.execute(f"Select * FROM {table} LIMIT 0")
        return [desc[0] for desc in cursor.description]

    def get_rows_count(self, cursor, table):
        cursor.execute(f"Select count(*) FROM {table}")
        return cursor.fetchone()[0]

    def diff_row(self, table, source_row, target_row, row_number):
        diff = {}
        # Check source row matches target row
        for key, value in source_row.items():
            target_value = None
            icon = "-"
            if target_row:
                icon = "~"
                target_value = target_row.pop(key, None)
            if target_value != value:
                diff[key] = {
                    "icon": icon,
                    "row number": row_number,
                    "column": key,
                    "source": value,
                    "target": target_value,
                }

        # Check there is more data available in target row and if so add it to the diff
        if target_row:
            for key, value in target_row.items():
                diff[key] = {
                    "icon": "+",
                    "row number": row_number,
                    "column": key,
                    "source": None,
                    "target": value,
                }
        return diff

    def apply_exclusions_to_columns(self, table, columns):
        return [f'"{column}"' for column in set(columns) - self.exclude_columns]

    def select_all(self, connection, table, columns):
        cols = self.apply_exclusions_to_columns(table, columns)

        cols = ",".join(sorted(cols))
        sql = f"SELECT {cols} FROM {table}"
        if "id" in columns:
            sql += " order by id"
        cursor = self.get_dict_cursor(connection)
        cursor.execute(sql)
        return cursor

    def diff_table(self, table):
        source_columns = self.get_columns(self.source_cursor, table)
        target_columns = self.get_columns(self.target_cursor, table)
        output = {
            "table present": table in self.target_tables,
            "columns equal": source_columns == target_columns,
            "row count": {
                "source": self.get_rows_count(self.source_cursor, table),
                "target": self.get_rows_count(self.target_cursor, table),
            },
            "diff": [],
        }
        source_cursor = self.select_all(self.source_conn, table, source_columns)
        target_cursor = self.select_all(self.target_conn, table, target_columns)
        rownumber = 0
        for index, source_row in enumerate(source_cursor):
            rownumber = index + 1
            target_row = target_cursor.fetchone()
            if source_row != target_row:
                output["diff"].append(
                    self.diff_row(table, source_row, target_row, rownumber)
                )

        if "rownumber" not in locals():
            rownumber = 0
        else:
            rownumber += 1
        # Check if there are more target rows
        for target_row in target_cursor:
            output["diff"].append(self.diff_row(table, {}, target_row, rownumber))
            rownumber += 1

        return output

    def log_table_diff(self, table, diffs):
        with open(f"{self.output_dir}/{table}.log", "w") as fh:
            headers = ["Icon", "Row", "Column", "Source", "Target"]
            rows = []
            for diff in diffs:
                for _, row in diff.items():
                    rows.append(
                        [
                            row["icon"],
                            row["row number"],
                            row["column"],
                            row["source"],
                            row["target"],
                        ]
                    )

            table = tabulate(rows, headers, tablefmt="simple_grid")
            fh.write(table)

    def diff_data(self):
        summary = []
        for table in self.source_tables:
            if table in self.exclude_tables:
                continue

            output = self.diff_table(table)
            if (
                not output["diff"]
                and output["row count"]["source"] == output["row count"]["target"]
            ):
                continue

            self.log_table_diff(table, output["diff"])

            summary.append(
                {
                    "table": table,
                    "table present": output["table present"],
                    "columns equal": output["columns equal"],
                    "source rows count": output["row count"]["source"],
                    "target rows count": output["row count"]["target"],
                    "counts equal": output["row count"]["source"]
                    == output["row count"]["target"],
                    "rows equal": len(output["diff"]) == 0,
                }
            )
        self.log_summary(summary)

    def log_summary(self, summary):
        headers = {
            "table": "Table",
            "table present": "In target",
            "columns equal": "Columns equal",
            "source rows count": "Source rows",
            "target rows count": "Target rows",
            "counts equal": "Counts equal",
            "rows equal": "Rows equal",
        }
        summary = tabulate(summary, headers=headers, tablefmt="simple_grid")
        with open(f"{self.output_dir}/summary.log", "w") as fh:
            fh.write(summary)
        print(summary)


if __name__ == "__main__":
    dsn1 = "postgres://postgres:postgres@prev_db:5432/cla_backend"
    dsn2 = "postgres://postgres:postgres@db:5432/cla_backend"

    exclude_columns = [
        "id",
        "created",
        "modified",
        "search_field",
        "reference",
        "patch",
        "notes",
        "context",
        "nodes",
    ]
    output_dir = os.path.join(os.environ.get("DATA_DIRECTORY", "/tmp"), "yapgdd")
    exclude_tables = [
        "oauth2_provider_refreshtoken",
        "auth_user",
        "oauth2_provider_accesstoken",
        "django_admin_log",
    ]
    diff = Yapgdd(
        dsn1,
        dsn2,
        exclude_columns=exclude_columns,
        exclude_tables=exclude_tables,
        output_dir=output_dir,
    )
    diff.diff_data()
