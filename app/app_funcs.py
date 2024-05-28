"""
    This module contains functions for the app.
"""

import re

import psycopg2
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


def load_sql(cursor, file):
    """
    Executes the SQL queries in the specified file using the provided database cursor.

    Parameters:
        cursor (psycopg2.extensions.cursor): The database cursor to use for executing the queries.
        file (str): The path to the file containing the SQL queries.

    Returns:
        None
    """

    with open(file, "r", encoding="utf-8") as file:
        sql_query = file.read()

        cursor.execute(sql_query)


def insert_data_from_line(cursor, line):
    """
    Inserts data from a single line into the database.

     Parameters:
        cursor (psycopg2.extensions.cursor): The database cursor to execute the SQL query.
        line (str): The line of data to be inserted.
                    Data in each line will be split by space.

    Returns:
        None
    """

    data_list = line.split(" ")

    created = " ".join(data_list[0:2])
    int_id = data_list[2]
    line_without_datetime = " ".join(data_list[2:]).strip()

    flag = data_list[3]

    if flag == "<=":
        flag_potential = data_list[4]

        if flag_potential != "<>":
            pos_1 = data_list[-1].find("id=")

            id_from_field = data_list[-1][pos_1 + 3 :].strip()

            cursor.execute(
                """
                INSERT INTO message (created, id, int_id, str)
                VALUES (TIMESTAMP %s, %s, %s, %s);
                """,
                (
                    created,
                    id_from_field,
                    int_id,
                    line_without_datetime,
                ),
            )
    else:
        flags_all = set(["<=", "=>", "->", "**", "=="])

        if flag in flags_all:
            address = data_list[4]
        else:
            address = None

        cursor.execute(
            """
            INSERT INTO log (created, int_id, str, address)
            VALUES (TIMESTAMP %s, %s, %s, %s);
            """,
            (
                created,
                int_id,
                line_without_datetime,
                address,
            ),
        )


def find_lines_with_email(cursor, email):
    """
    Retrieves the first 101 lines from the 'message' and 'log' tables
    that contain the specified email address.

    Parameters:
        cursor (psycopg2.extensions.cursor): The database cursor to execute the SQL query.
        email (str): The email address to search for.

    Returns:
        dict: A dictionary containing the retrieved lines and the count of lines.
        The dictionary has the following structure:
            - rows (list): A list of tuples, where each tuple represents
                a line and contains the 'created' timestamp and the 'str' column value.
            - count (int): The total number of retrieved lines.
    """
    cursor.execute(
        """
        WITH data AS
        (
            SELECT int_id, created, str
            FROM message
            WHERE str like '%%' || %s || '%%'
            UNION ALL
            SELECT int_id, created, str
            FROM log
            WHERE address = %s
        )
        SELECT created, str
        FROM data
        ORDER BY int_id, created
        LIMIT 101;
        """,
        (
            email,
            email,
        ),
    )

    result = {"rows": [], "count": 0}

    for row in cursor:
        result["rows"].append(row)
        result["count"] += 1

    return result


def connect_to_db():
    """
    Connects to a PostgreSQL database using the provided credentials.

    Returns:
        tuple: A tuple containing the database connection object and the cursor object.
               If an error occurs during the connection, returns (None, None).

    Raises:
        Exception: If an error occurs while connecting to the database.
        psycopg2.DatabaseError: If an error occurs while connecting to the database.

    """

    try:
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        conn.autocommit = True

        cur = conn.cursor()
        return conn, cur
    except Exception as error:
        print("Error connecting to PostgreSQL database: ", error)
        return None, None


def check_email(email):
    """
    Check if the given email address is valid.

    Parameters:
        email (str): The email address to be checked.

    Returns:
        True or False
    """
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    return re.fullmatch(regex, email)
