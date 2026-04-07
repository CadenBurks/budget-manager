from parsers.pnc_parser import PNCParser
from analysis.ledger import generate_monthly_summaries
from pathlib import Path
from rich.pretty import pprint

parser = PNCParser()
transactions = parser.parse_transactions(Path('test_year.csv'), [])
summaries = generate_monthly_summaries(transactions)

for date, summary in summaries.items():
    print(f"{date}: income={summary.income}, expenses={summary.expenses}, net={summary.net}")