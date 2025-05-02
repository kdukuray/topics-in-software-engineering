"""
Unit Tests that I added as part of my second submission.
Tests a new function I made that verifies if a withdrawal is valid or not.
"""
from decimal import Decimal
from ..utils import can_withdraw
def test_can_withdraw_valid():
    assert can_withdraw(Decimal('100.00'), Decimal('50.00')) is True

def test_can_withdraw_exact():
    assert can_withdraw(Decimal('25.00'), Decimal('25.00')) is True

def test_can_withdraw_insufficient():
    assert can_withdraw(Decimal('10.00'), Decimal('20.00')) is False

def test_can_withdraw_zero_amount():
    assert can_withdraw(Decimal('10.00'), Decimal('0.00')) is False

def test_can_withdraw_negative_amount():
    assert can_withdraw(Decimal('10.00'), Decimal('-5.00')) is False
