import requests
import json
from config import keys

class APIExeption(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise APIExeption(f'Невозможно перевести одинаковые валюты {quote}.')
    
        try: 
            base_ticker = keys[base.lower()]

        except KeyError:
            raise APIExeption(f'Не удалось обработать валюту {base}.')
    
        try: 
            quote_ticker = keys[quote.lower()]
    
        except KeyError:
            raise APIExeption(f'Не удалось обработать валюту {quote}.')
    
        try:
            amount = float(amount)
            
        except ValueError:
            raise APIExeption(f'Не удалось обработать количество {amount}.')
        
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_quote = json.loads(r.content)[keys[quote.lower()]] * amount

        return total_quote