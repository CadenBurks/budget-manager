from parsers.pnc_parser import PNCParser
from analysis.ledger import generate_monthly_summaries
from pathlib import Path
from rich.pretty import pprint
import csv

parser = PNCParser()
transactions = parser.parse_transactions(Path('test_year.csv'), [])
for t in transactions:
    pprint(t)
# summaries = generate_monthly_summaries(transactions)

# for date, summary in summaries.items():
#     print(f"{date}: income={summary.income}, expenses={summary.expenses}, net={summary.net}")

# cats = set()
# with open(Path('test_year.csv'), newline='') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         cats.add(row['Category'])

# pprint(cats)