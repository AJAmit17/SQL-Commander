import sqlite3
import streamlit as st

def execute_user_sql_queries(queries):
    """
    Execute the given SQL queries using the sqlite3 database connection.

    Args:
        queries (str): The SQL queries to be executed.

    Returns:
        None
    """
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()

    cursor.executescript(queries)

    conn.commit()
    conn.close()

def main():
    """
    This function sets the page configuration, sets the title of the page, 
    takes SQL queries as input from the user, executes the queries on an SQLite 
    database, and displays success or error messages based on the execution 
    result.
    """
    st.set_page_config(page_title="sql query executor")
    st.title("SQLite Query Executor")

    queries = st.text_area("Enter SQL queries here:", "", height=200)

    if st.button("Execute Queries"):
        try:
            execute_user_sql_queries(queries)

            st.success("SQL queries executed successfully!")
        except Exception as e:
            st.error(f"Error executing SQL queries: {str(e)}")

if __name__ == "__main__":
    main()