# StellarStmt: Bank Statement Processor

A Python application that processes Excel bank statements and stores them in an SQLite database for easy querying and analysis.

## Features
- Processes Excel files (.xlsx, .xls) containing bank transaction data
- Stores transactions in a structured SQLite database
- Tracks file metadata including upload timestamps and source filenames
- Maintains data integrity with proper schema management
- Provides a simple menu-driven interface for user interaction
- Handles timezone-aware timestamps (UTC)
- Supports future expansion with additional metadata fields

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (optional but recommended)

### Steps
1. Clone this repository
2. Navigate to the project directory:
   ```bash
   cd stellar-stmt
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python src/main.py
   ```
2. Use the menu to select an option:
   - `1`: Process Excel folder - Import bank statements from Excel files
   - `2`: Read from database - View stored transactions
   - `3`: Init/Reinit database - Reset database (deletes all data)

### Excel File Requirements
- Supported formats: .xlsx, .xls
- Expected columns: Date, Category, Description, Account, Amount, Currency, Split

## Project Structure
```
stellar-stmt/
├── src/
│   ├── database.py    # Database operations and schema management
│   └── main.py        # Main application logic and menu interface
├── statements.db      # SQLite database (created on first run)
├── requirements.txt   # Project dependencies
└── README.md          # Project documentation
```

## Database Schema
The application maintains a `bank_statements` table with the following structure:
- `id`: Future use for unique transaction identification
- `status`: Future use for transaction status tracking
- `notes`: Future use for user notes
- `uploaded_by`: User who uploaded the transaction
- `uploaded_time`: UTC timestamp of upload
- `file_name`: Source Excel filename
- `transaction_date`: Date of the transaction
- `transaction_category`: Category classification
- `transaction_description`: Transaction details
- `account_name`: Account associated with the transaction
- `transaction_amount`: Monetary amount
- `transaction_currency`: Currency type
- `split_status`: Split transaction indicator

## Troubleshooting
- **Excel Import Issues**: Ensure files follow the required format and columns
- **Database Errors**: Use option 3 to reinitialize the database schema
- **Timezone Concerns**: All timestamps are stored in UTC for consistency

## License
[MIT License](LICENSE)