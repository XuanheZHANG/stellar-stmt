import bank_stmt_db as bank_stmt_db
from hsbc_processor import HSBCBankStmtProcessor

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
        processor = HSBCBankStmtProcessor()
        processor.process()
    elif choice == '3':
        print("ICBC processing coming soon")    
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