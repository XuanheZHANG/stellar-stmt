import pandas as pd
import os
import glob
import bank_stmt_db as bank_stmt_db
from transaction_model import TransactionRecord

class HSBCBankStmtProcessor:
    def __init__(self):
        self.folder_path = os.getenv('STATEMENTS_HSBC_PATH')
    
    def process(self):
        if not os.path.isdir(self.folder_path):
            print(f"Error: '{self.folder_path}' is not a valid directory")
            return
            
        excel_files = glob.glob(os.path.join(self.folder_path, '*.[xX][lL][sS]*'))
        clean_files = [f for f in excel_files if not os.path.basename(f).startswith('~$')]
        
        for file in clean_files:
            try:
                df = pd.read_excel(file, engine='openpyxl' if file.lower().endswith('.xlsx') else 'xlrd')
                transaction_records = TransactionRecord.from_hsbc_dataframe(df, os.path.basename(file), os.getenv('CURRENT_USER'))
                bank_stmt_db.save_to_sqlite(transaction_records, if_exists='append')
            except Exception as e:
                print(f"Error processing {file}: {e}")
