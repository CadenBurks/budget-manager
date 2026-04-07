import csv
from datetime import date
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class MonthlySummary:
    month: int
    income: Decimal = Decimal(0)
    expenses: Decimal = Decimal(0)
    
    @property
    def net(self) -> Decimal:
        return self.income - self.expenses

class SummaryDict(defaultdict):
    def __missing__(self, key):
        summary = MonthlySummary(key)
        self[key] = summary
        return summary

def clean_amount(amount: str) -> list:
    amount = amount.replace(" ", "")
    amount = amount.replace("$", "")
    sign = amount[0]
    value = amount[1:]
    return [sign, Decimal(value)]

monthly_summaries = SummaryDict(MonthlySummary)

with open('test.csv', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        transaction_month = date.fromisoformat(row['Transaction Date']).month
        summary = monthly_summaries[transaction_month]
        amount = row['Amount']
        sign, value = clean_amount(amount)

        if sign == "+":
            summary.income += value
        else:
            summary.expenses += value

for k, v in monthly_summaries.items():
    print(k, v, v.net)