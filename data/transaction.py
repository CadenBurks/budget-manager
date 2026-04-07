from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum
from data.category import Category

class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"

@dataclass(frozen=True)
class Transaction:
    transaction_date: date
    raw_desc: str
    merchant: str
    amount: Decimal
    transaction_type: TransactionType
    category: Category
    balance: Decimal | None = field(default=None)
