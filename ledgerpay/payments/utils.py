from decimal import Decimal

def can_transfer(balance: Decimal, amount: Decimal) -> bool:
    """
    Returns True if balance is enough and amount is positive.
    """
    return balance >= amount and amount > 0
