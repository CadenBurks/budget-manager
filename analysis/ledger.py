from data.summary import MonthlySummary, SummaryDict
from data.transaction import Transaction, TransactionType

def generate_monthly_summaries(transactions: list[Transaction]) -> SummaryDict:
    monthly_summaries = SummaryDict(MonthlySummary)

    for transaction in transactions:
        summary_date = (transaction.transaction_date.year, transaction.transaction_date.month)
        summary = monthly_summaries[summary_date]
        
        if transaction.transaction_type == TransactionType.INCOME:
            summary.income += transaction.amount
        else:
            summary.expenses += transaction.amount
        
        summary.transactions.append(transaction)
    
    return monthly_summaries