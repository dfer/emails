"""
This file contains the main logic for example app.
"""

import app_funcs
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    """
    This function is a route handler for the root URL ("/") of the Flask application.
    It renders the "index.html" template and returns the rendered HTML as a response.

    Parameters:
        None

    Returns:
        The rendered HTML template as a Flask response.
    """
    return render_template("index.html")


@app.route("/install")
def install():
    """
    Install route handler for the Flask application.

    This function is responsible for handling the "/install" route.
    It connects to the database using the `connect_to_db` function from the `app_funcs` module.
    If the connection is successful, it calls the `load_sql` function to load an SQL file.
    The database connection and cursor are then closed.

    Returns:
        str: The string "Install successfull" indicating the success of the installation.
        str: The string "Install failed" indicating the not success of the installation.
    """

    conn, cur = app_funcs.connect_to_db()
    if conn is not None:
        app_funcs.load_sql(cur, "db/install.sql")

        # Open and read the text file line by line
        with open("data/out", "r", encoding="utf-8") as file:
            for line in file:
                app_funcs.insert_data_from_line(cur, line)

        cur.close()
        conn.close()

        return "Install successfull"

    return "Install failed"


@app.route("/uninstall")
def uninstall():
    """
    Uninstall route handler for the Flask application.

    This function is responsible for handling the "/uninstall" route.
    It connects to the database using the `connect_to_db` function from the `app_funcs` module.
    If the connection is successful, it calls the `load_sql` function to load an SQL file.
    The database connection and cursor are then closed.

    Returns:
        str: The string "Uninstall successfull" indicating the success of the uninstallation.
        str: The string "Uninstall failed" indicating the not success of the uninstallation.
    """

    conn, cur = app_funcs.connect_to_db()
    if conn is not None:
        app_funcs.load_sql(cur, "db/uninstall.sql")

        cur.close()
        conn.close()

        return "Uninstall successfull"

    return "Uninstall failed"


@app.route("/submit", methods=["POST"])
def submit():
    """
    Submit email for find it in db.

    Returns:
        str: The rendered HTML template with the found lines as the context.
        str: The string "No email provided" if the email is not provided or is invalid.
        str: The string "Connection failed" if the connection to the database fails.
    """
    email = request.values.get("email")

    if not app_funcs.check_email(email):
        return "No email provided"

    conn, cur = app_funcs.connect_to_db()
    if conn is not None:
        result = app_funcs.find_lines_with_email(cur, email)

        cur.close()
        conn.close()

        return render_template("result.html", context=result)

    return "Connection failed"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4567)
