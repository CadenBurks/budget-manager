from parsers.bank_parser import BankParser
from data.transaction import Transaction, TransactionType
from data.category import Category, CategoryMap
from datetime import date
from decimal import Decimal
import re

PNC_PREFIXES = [
    "DEBIT CARD PURCHASE ",
    "RECURRING DEBIT CARD ",
    "ONLINE TRANSFER FROM ",
    "ONLINE TRANSFER TO ",
    "ATM DEPOSIT ",
    "MOBILE DEPOSIT ",
    "ZELLE TO ",
    "ZELLE FROM ",
    "ZEL TO ",
    "ZEL FROM ",
]
PNC_CATEGORY_MAP = CategoryMap({
    "": Category.UNCATEGORIZED,
    "Other Expenses": Category.UNCATEGORIZED,
    "Paychecks": Category.PAYCHECK,
    "Deposits": Category.DEPOSIT,
    "Home Maintenance": Category.HOME,
    "Home Improvement": Category.HOME,
    "Phone": Category.PHONE,
    "Transfers": Category.UNCATEGORIZED_TRANSFER,
    "Cash Withdrawals": Category.WITHDRAWAL,
    "Education": Category.SERVICES,
    "Services and Supplies": Category.SERVICES,
    "Subscriptions and Renewals": Category.SUBSCRIPTIONS,
    "Clothing and Shoes": Category.CLOTHING,
    "Auto Maintenance": Category.AUTO,
    "Entertainment": Category.ENTERTAINMENT,
    "Restaurants and Dining": Category.DINING_AND_DELIVERY,
    "Utilities": Category.UTILITIES,
    "Gas and Fuel": Category.GAS,
    "Hobbies": Category.SHOPPING,
    "General Merchandise": Category.SHOPPING,
    "Electronics": Category.DIGITAL,
    "Other Income": Category.OTHER_INCOME,
    "Rewards": Category.OTHER_INCOME,
    "Insurance": Category.INSURANCE,
    "Personal Expenses": Category.GYM,
    "Groceries": Category.GROCERIES
})
STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", 
    "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", 
    "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", 
    "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", 
    "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", 
    "VT", "VA", "WA", "WV", "WI", "WY"
}
POS_PURCHASE = "POS PURCHASE"


class PNCParser(BankParser):
    def _convert_date(self, transaction_date: str) -> date:
        return date.fromisoformat(transaction_date)

    def _strip_noise(self, tokens: list) -> list:
        to_remove = set()
        for i in range(len(tokens) - 1, -1, -1):
            if i == 0:
                continue
            if tokens[i] in STATES:
                to_remove.add(i)
                if i > 0:
                    to_remove.add(i - 1)
            # pattern for digits
            elif re.search(r"^[0-9]+$", tokens[i]):
                to_remove.add(i)
            # pattern for letters and digits
            elif re.search(r"^(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9]+$", tokens[i]):
                to_remove.add(i)
            # pattern for phone numbers
            elif re.search(r"^[0-9-]+$", tokens[i]):
                to_remove.add(i)
            # pattern for account numbers and ref codes
            elif re.search(r"[x]+[0-9]+", tokens[i]):
                to_remove.add(i)
            # pattern for urls
            elif re.search(r"\.[a-zA-Z]{2,}", tokens[i]):
                to_remove.add(i)
        
        return [token for j, token in enumerate(tokens) if j not in to_remove]

    def _clean_desc(self, desc: str) -> str:
        original = desc
        if POS_PURCHASE in desc:
            # pattern for POS codes
            desc = re.sub(r"POS[a-zA-Z0-9]+", "", desc)
            desc = re.sub(POS_PURCHASE, "", desc)
            desc = re.sub("POS", "", desc).strip()
        else:
            for prefix in PNC_PREFIXES:
                if desc.startswith(prefix):
                    desc = desc.removeprefix(prefix).strip()
                    desc = re.sub(r"[xX]+[0-9]+", "", desc).strip()
                    break
        tokens = self._strip_noise(desc.split())
        result = " ".join(tokens)
        return result if result.strip() else original

    def _parse_amount(self, amount: str) -> tuple[Decimal, TransactionType]:
        amount = amount.replace(" ", "")
        amount = amount.replace("$", "")
        transaction = amount[0]
        value = amount[1:]

        if transaction == "+":
            transaction = TransactionType.INCOME
        else:
            transaction = TransactionType.EXPENSE

        return (Decimal(value), transaction)

    def _categorize(self, merchant: str, raw_desc: str, category: str, rules: list) -> Category:
        if rules:
            for rule in rules:
                match = rule["match"].upper()
                if match in merchant.upper() or match in raw_desc.upper():
                    try:
                        return Category[rule["category"].upper().replace(" ", "_")]
                    except KeyError:
                        print(f"Unknown category in rules: {rule['category']}")
                        return Category.UNCATEGORIZED

        return PNC_CATEGORY_MAP[category]

    def _parse_balance(self, balance: str) -> Decimal:
        return Decimal(balance[1:])

    def parse_transaction(self, row: dict, rules: list) -> Transaction:
        transaction_date = self._convert_date(row['Transaction Date'])
        raw_desc = row['Transaction Description']
        merchant = self._clean_desc(raw_desc)
        amount, transaction_type = self._parse_amount(row['Amount'])
        category = self._categorize(merchant, raw_desc, row['Category'], rules)
        balance_raw = row.get('Balance')
        balance = self._parse_balance(balance_raw) if balance_raw else None
        
        return Transaction(
            transaction_date = transaction_date,
            raw_desc = raw_desc,
            merchant = merchant,
            amount = amount,
            transaction_type = transaction_type,
            category = category,
            balance = balance
        )
