from abc import ABC, abstractmethod
from data.transaction import Transaction
from pathlib import Path
import csv

class BankParser(ABC):
    @abstractmethod
    def parse_transaction(self, row: dict, rules: list) -> Transaction:
        pass

    def parse_transactions(self, path: Path, rules: list) -> list[Transaction]:
        transactions = []
        with open(path, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append(self.parse_transaction(row, rules))

        return transactions
