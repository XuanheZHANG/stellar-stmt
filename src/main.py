import pandas as pd
import os
import glob
from dotenv import load_dotenv
from database import save_to_sqlite, read_from_sqlite, clear_data_in_sqlite

# 加载环境变量
load_dotenv()

table_name = 'bank_statements'
folder_path = '/Users/xuanhezhang/Downloads/statements'
current_user = 'Mao Mao Niu'

def process_excel_folder(folder_path):
    """Process all Excel files in a folder and save to SQLite"""
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory")
        return
    else:
        # Get all Excel files in the folder (both .xlsx and .xls)
        excel_files = glob.glob(os.path.join(folder_path, '*.xlsx')) + \
                      glob.glob(os.path.join(folder_path, '*.xls')) + \
                      glob.glob(os.path.join(folder_path, '*.XLSX')) + \
                      glob.glob(os.path.join(folder_path, '*.XLS'))
        
        # Filter out temporary Excel files that start with "~$"
        excel_files = [f for f in excel_files if not os.path.basename(f).startswith('~$')]
        if not excel_files:
            print(f"Error: No Excel files found in '{folder_path}'")
            print("Supported file formats: .xlsx, .xls")
            return

        # Process each Excel file
        for file in excel_files:
            try:
                file_name = os.path.basename(file)
                # Read Excel file
                print(f"Reading file: {file_name}")
                # Determine engine based on file extension
                if file.lower().endswith('.xlsx'):
                    engine = 'openpyxl'
                elif file.lower().endswith('.xls'):
                    engine = 'xlrd'
                else:
                    print(f"Unsupported file format: {file_name}")
                    continue
                df = pd.read_excel(file, engine=engine)
                # Get table name from file name (remove extension)
                # Use single table for all Excel files]
                # Save to SQLite with append mode
                print(f"Processing file: {file_name}")
                save_to_sqlite(df, table_name, file_name, current_user, if_exists='append')
            except Exception as e:
                print(f"Error processing file {file}: {e}")

def main():
    print("Python project initialized successfully!")
    print("Supported features:")
    print("1. Process Excel folder and save to SQLite database")
    print("2. Read data from SQLite database")
    print("3. Init/Reinit transaction table")
    
    choice = input("Please enter your choice (1 or 2 or 3): ")
    if choice == '1':
        process_excel_folder(folder_path)
    elif choice == '2':
        read_from_sqlite(table_name)
    elif choice == '3':
        clear_data_in_sqlite(table_name)
        print(f"Database {table_name} reinitialized successfully!")
    else:
        print("Invalid choice. Please enter 1 or 2 or 3.")

if __name__ == "__main__":
    main()