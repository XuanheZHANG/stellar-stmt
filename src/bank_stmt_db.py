import sqlite3
import pandas as pd
from transaction_model import TransactionRecord

# Module-level configuration
table_name = 'bank_statements'
BANK_STMT_COLUMN_DEF = {
    'date': 'INTEGER', #YYYYMMDD
    'category': 'TEXT',
    'description': 'TEXT',
    'account': 'TEXT',
    'amount': 'REAL',
    'currency': 'TEXT',
    'note': 'TEXT',
    'invoice_receipt': 'TEXT',
    'file_name': 'TEXT',
    'updated_by': 'TEXT',
    'updated_time': 'INTEGER' #Unix epoch milliseconds
}

# Database operations as functions
def create_connection(db_name='statements.db'):
    return sqlite3.connect(db_name)

def init_table():
    connection = create_connection()
    connection.execute(f"DROP TABLE IF EXISTS {table_name}")
    create_table_query = f"CREATE TABLE {table_name} ({', '.join([f'{col} {type}' for col, type in BANK_STMT_COLUMN_DEF.items()])})"
    try:
        connection.execute(create_table_query)
        connection.commit()
    except Exception as e:
        print(f"Error creating table: {e}")
        connection.rollback()
    finally:
        connection.close()

def save_to_sqlite(df, file_name, current_user, if_exists='replace'):
    """Save DataFrame to SQLite database table"""
    connection = create_connection()
    try:
        if if_exists == 'replace':
            clear_data_in_sqlite(table_name)

        # prepare insert query
        sorted_columns = sorted(list(BANK_STMT_COLUMN_DEF.keys()))
        columns = ', '.join(sorted_columns)
        placeholders = ', '.join(['?'] * len(sorted_columns))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        transaction_records = TransactionRecord.from_hsbc_dataframe(df, file_name, current_user)
        # Convert TransactionRecords to dictionaries first
        if (isinstance(transaction_records, list) 
            and len(transaction_records) > 0 
            and isinstance(transaction_records[0], TransactionRecord)):
            dict_trans_records = [r.__dict__ for r in transaction_records]
        data_to_insert = [tuple(row[col] for col in sorted_columns) for row in dict_trans_records]
        connection.executemany(insert_query, data_to_insert)
        connection.commit() 
        print(f"Data saved to {table_name} table in SQLite database.")
    except Exception as e:
        print(f"Error saving data to SQLite database: {e}")
    finally:
        connection.close()

def read_from_sqlite(output_path='output.xlsx'):
    """Read data from SQLite database table"""
    connection = create_connection()
    try:
        # check if table exists
        cursor = connection.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if cursor.fetchone() is None:
            print("No data to export.")
            return None
        
        # get data from table
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", connection)        
        if df.empty:
            print("No data to export.")
        else:
            df.to_excel(output_path)
            print(f"Data exported to {output_path}")
        return df
    except Exception as e:
        print(f"Error reading data from SQLite database: {e}")
    finally:
        connection.close()

def clear_data_in_sqlite(file_name=''):
    connection = create_connection()
    try:
        if file_name:
            connection.execute(f"DELETE FROM {table_name} WHERE file_name = ?", (file_name,))
            print(f"Deleted data from {table_name} where file_name = {file_name}")
        else:
            connection.execute(f"DELETE FROM {table_name}")
            print(f"Deleted all data from {table_name}")
        connection.commit()  # Explicitly commit the transaction
        print(f"Data cleared from {table_name} table in SQLite database.")
    except Exception as e:
        connection.rollback()  # Rollback on error
        print(f"Error clearing data from SQLite database: {e}")    
    finally:
        connection.close()

