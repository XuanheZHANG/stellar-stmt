import sqlite3
import pandas as pd

def create_connection(db_name='statements.db'):
    return sqlite3.connect(db_name)

# Column mapping configuration (Excel column name -> Database column name)
COLUMN_MAPPING = {
    'Date': 'transaction_date',
    'Category': 'category',
    'Description': 'description',
    'Account': 'account',
    'Amount': 'amount',
    'Currency': 'currency',
    'Note': 'notes',
    'Invoice/receipt': 'invoice_receipt'
}

def save_to_sqlite(df, table_name, file_name, current_user, if_exists='replace'):
    """Save DataFrame to SQLite database table"""
    connection = create_connection()
    try:
        # Apply column name mapping
        df = df.rename(columns=COLUMN_MAPPING)
        
        # Add metadata columns to every row
        df = df.assign(
            file_name=file_name,
            current_user=current_user,
            updated_time=pd.Timestamp.now().to_pydatetime()
        )
        
        # Get column names
        columns = ', '.join(df.columns)

        # Create placeholders
        placeholders = ', '.join(['?'] * len(df.columns))
        
        # Get final column names after all transformations
        final_columns = df.columns.tolist()
        
        if if_exists == 'replace':
            connection.execute(f"DROP TABLE IF EXISTS {table_name}")
            create_table_query = f"CREATE TABLE {table_name} ({', '.join([f'{col} TEXT' for col in final_columns])})"
            connection.execute(create_table_query)
        elif if_exists == 'append':
            # If table exists, check if all columns already exist
            cursor = connection.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            existing_columns = [col[1] for col in cursor.fetchall()]
            
            # Check against final column names
            if set(existing_columns) != set(final_columns):
                print(f"Warning: Columns in DataFrame do not match existing table {table_name}. Data will be appended with empty columns.")
                # Add missing columns
                for col in final_columns:
                    if col not in existing_columns:
                        try:
                            connection.execute(f"ALTER TABLE {table_name} ADD COLUMN {col} TEXT")
                            print(f"Adding Missing Column ({col}) in DB")
                        except sqlite3.OperationalError as e:
                            if "duplicate column name" in str(e):
                                print(f"Column {col} already exists, skipping")
                            else:
                                raise
        
        # 插入数据
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        try:
            # Convert all DataFrame values to native Python types
            data_to_insert = [tuple(row.astype(str) if hasattr(row, 'astype') else row) 
                             for _, row in df.iterrows()]
            
            connection.executemany(insert_query, data_to_insert)
            connection.commit()  # Explicitly commit the transaction
            print(f"Data saved to {table_name} table in SQLite database.")
        except Exception as e:
            connection.rollback()  # Rollback on error
            raise
    except Exception as e:
        print(f"Error saving data to SQLite database: {e}")
    finally:
        connection.close()

def read_from_sqlite(table_name, output_path='output.xlsx'):
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

def clear_data_in_sqlite(table_name):
    """Clear data from SQLite database table"""
    connection = create_connection()
    try:
        connection.execute(f"DROP TABLE IF EXISTS {table_name}")
        connection.commit()  # Explicitly commit the transaction
        print(f"Data cleared from {table_name} table in SQLite database.")
    except Exception as e:
        connection.rollback()  # Rollback on error
        print(f"Error clearing data from SQLite database: {e}")    
    finally:
        connection.close()
