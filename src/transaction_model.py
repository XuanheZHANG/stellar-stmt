from datetime import datetime

class TransactionRecord:
    """
    Bank transaction record data model
    """
    
    # Define field mapping (Excel column name -> Model property name)
    HSBC_FIELD_MAPPING = {
        'Date': 'date',
        'Category': 'category',
        'Description': 'description',
        'Account': 'account',
        'Amount': 'amount',
        'Currency': 'currency',
        'Note': 'note',
        'Invoice/receipt': 'invoice_receipt'
    }
    
    def __init__(self, **kwargs):
        """
        init transaction record
        """
        self.date = kwargs.get('date')  # YYYYMMDD Integer
        self.category = kwargs.get('category', '')
        self.description = kwargs.get('description', '')
        self.account = kwargs.get('account', '')
        self.amount = kwargs.get('amount', 0.0)
        self.currency = kwargs.get('currency', '')
        self.note = kwargs.get('note', '')
        self.invoice_receipt = kwargs.get('invoice_receipt', '')
        self.file_name = kwargs.get('file_name', '')
        self.updated_by = kwargs.get('updated_by', '')
        self.updated_time = kwargs.get('updated_time', int(datetime.now().timestamp() * 1000))  # Unix Epoch Milliseconds
    
    @classmethod
    def from_hsbc_dataframe(cls, df, file_name, current_user):
        """
        Create a list of TransactionRecord objects from a DataFrame
        """
        records = []
        for _, row in df.iterrows():
            record_data = {
                'file_name': file_name,
                'updated_by': current_user
            }
            
            # Map DataFrame columns to model fields
            for excel_col, field in cls.HSBC_FIELD_MAPPING.items():
                if excel_col in row:
                    record_data[field] = row[excel_col]
            
            records.append(cls(**record_data))
        return records
    
    def to_dict(self):
        """
        Convert the object to a dictionary
        """
        return {
            'date': self.date,
            'category': self.category,
            'description': self.description,
            'account': self.account,
            'amount': self.amount,
            'currency': self.currency,
            'note': self.note,
            'invoice_receipt': self.invoice_receipt,
            'file_name': self.file_name,
            'updated_by': self.updated_by,
            'updated_time': self.updated_time
        }