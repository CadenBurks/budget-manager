from enum import Enum

class Category(Enum):
    PAYCHECK = "Paycheck"
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"
    OTHER_INCOME = "Other Income"
    RENT = "Rent"
    UTILITIES = "Utilities"
    PHONE = "Phone"
    SUBSCRIPTIONS = "Subscriptions"
    ENTERTAINMENT = "Entertainment"
    GROCERIES = "Groceries"
    GAS = "Gas"
    AUTO = "Auto"
    INSURANCE = "Insurance"
    HOME = "Home"
    DINING_AND_DELIVERY = "Dining and Delivery"
    SHOPPING = "Shopping"
    CLOTHING = "Clothing"
    SERVICES = "Services"
    GYM = "Gym"
    DIGITAL = "Digital"
    UNCATEGORIZED_TRANSFER = "Uncategorized Transfer"
    UNCATEGORIZED = "Uncategorized"

class CategoryMap(dict):
    def __missing__(self, key):
        self[key] = Category.UNCATEGORIZED
        return Category.UNCATEGORIZED