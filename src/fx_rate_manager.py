import csv
from pathlib import Path
from typing import Dict

class FXRateManager:
    _rates: Dict[str, float] = {}

    @classmethod
    def load_static_rates(cls, file_path: str):
        """Load static FX rates from CSV file"""
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                pair = f"{row['from_currency']}/{row['to_currency']}"
                cls._rates[pair] = float(row['rate'])

    @classmethod
    def get_fx_rate(cls, from_currency: str, to_currency: str) -> float:
        """Get exchange rate for currency pair"""
        pair = f"{from_currency}/{to_currency}"
        if pair not in cls._rates:
            raise ValueError(f"No rate available for {pair}")
        return cls._rates[pair]

    @classmethod
    def convert_currency(cls, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert amount between currencies"""
        rate = cls.get_fx_rate(from_currency, to_currency)
        return round(amount * rate, 2)


def initialize_fx_rates():
    # Load default rates on module import
    default_rates = Path(__file__).parent.parent / 'fx_rates.csv'
    FXRateManager.load_static_rates(str(default_rates))

initialize_fx_rates()