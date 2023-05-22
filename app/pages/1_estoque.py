import sqlite3
import streamlit as st
import pandas as pd


# Function to create a SQLite database and table
def create_table():
    conn = sqlite3.connect("excel_data.db")
    cursor = conn.cursor()

    # Create a table to store Excel data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS excel_tables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT,
            data BLOB
        )
    """)

    conn.commit()
    conn.close()


# Function to save Excel tables to SQLite database
def save_excel_tables(file):
    conn = sqlite3.connect("excel_data.db")
    cursor = conn.cursor()

    # Read Excel file and store each table in the database
    excel_data = pd.read_excel(file, sheet_name=None)
    for sheet_name, df in excel_data.items():
        # Convert dataframe to binary format
        df_binary = df.to_pickle(None)
        df_bytes = df_binary.to_bytes()

        # Save table to the database
        cursor.execute("""
            INSERT INTO excel_tables (table_name, data)
            VALUES (?, ?)
        """, (sheet_name, df_bytes))

    conn.commit()
    conn.close()


# Function to retrieve Excel tables from SQLite database
def get_excel_tables():
    conn = sqlite3.connect("excel_data.db")
    cursor = conn.cursor()

    # Retrieve all tables from the database
    cursor.execute("""
        SELECT table_name, data
        FROM excel_tables
    """)
    results = cursor.fetchall()

    conn.close()

    # Convert binary data back to dataframes
    tables = []
    for table_name, data in results:
        df_bytes = pd.read_pickle(data)
        df = pd.read_pickle(df_bytes)
        tables.append((table_name, df))

    return tables


# Streamlit app
def main():
    st.title("Excel File Viewer")

    # Create the database table if it doesn't exist
    create_table()

    # File upload section
    st.subheader("Upload Excel File")
    file = st.file_uploader("Select an Excel file", type=["xlsx"])

    if file is not None:
        # Save the uploaded Excel file
        save_excel_tables(file)

        # Display the uploaded tables
        tables = get_excel_tables()
        for table_name, df in tables:
            st.subheader(f"Table: {table_name}")
            st.dataframe(df)


if __name__ == "__main__":
    main()
