from rich.pretty import pprint
from parsers.pnc_parser import PNCParser
from pathlib import Path

parser = PNCParser()
transactions = parser.parse_transactions(Path('test_year.csv'), [])

for t in transactions:
    pprint(t)