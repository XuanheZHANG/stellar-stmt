import pandas as pd
import os
import glob
from dotenv import load_dotenv
import bank_stmt_db as bank_stmt_db

# 加载环境变量
load_dotenv()

folder_path_hsbc = '/Users/xuanhezhang/Downloads/statements'
folder_path_icbc = '/Users/xuanhezhang/Downloads/statements_icbc'
current_user = 'Xuanhe'

def process_hsbc_bank_stmt(folder_path):
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
                bank_stmt_db.save_to_sqlite(df, file_name, current_user, if_exists='append')
            except Exception as e:
                print(f"Error processing file {file}: {e}")

def main():
    print("Python project initialized successfully!")
    print("Supported features:")
    print("1. Init Bank Statement Table Structure")
    print("2. Process HSBC Excel Bank Statement Folder and Save to SQLite database")
    print("3. Prooces ICBC Excel Bank Statement Folder and Save to SQLite database")
    print("4. Read data from SQLite database")
    print("5. Clear All Data in Transaction Table")
    print("6. Clear Data in Transaction Table for the Given File Name")
    
    
    choice = input("Please enter your choice [1-6]: ")
    if choice == '1':
        bank_stmt_db.init_table()
    elif choice == '2':
        process_hsbc_bank_stmt(folder_path_hsbc)
    elif choice == '3':
        process_hsbc_bank_stmt(folder_path_icbc)    
    elif choice == '4':
        bank_stmt_db.read_from_sqlite()
    elif choice == '5':
        bank_stmt_db.clear_data_in_sqlite()
    elif choice == '6':
        file_name = input("Please enter the file name: ")
        bank_stmt_db.clear_data_in_sqlite(file_name)
    else:
        print("Invalid choice. Please enter [1-6].")

if __name__ == "__main__":
    main()