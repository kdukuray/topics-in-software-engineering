from decimal import Decimal

def can_withdraw(balance: Decimal, amount: Decimal) -> bool:
    """
    Returns True if the wallet has enough balance to withdraw the given amount.
    """
    return balance >= amount and amount > Decimal("0.00")
