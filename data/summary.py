from collections import defaultdict
from dataclasses import dataclass, field
from decimal import Decimal
from data.transaction import Transaction

@dataclass
class MonthlySummary:
    summary_date: tuple[int, int]
    income: Decimal = Decimal(0)
    expenses: Decimal = Decimal(0)
    transactions: list[Transaction] = field(default_factory=list)
    
    @property
    def net(self) -> Decimal:
        return self.income - self.expenses

class SummaryDict(defaultdict):
    def __missing__(self, key):
        summary = MonthlySummary(key)
        self[key] = summary
        return summary
