"""These are our unit tests for the utility 'can_transfer function'"""

import unittest
from decimal import Decimal
from ..utils import can_transfer

class CanTransferTestCase(unittest.TestCase):

    def test_sufficient_balance(self):
        self.assertTrue(can_transfer(Decimal("100.00"), Decimal("50.00")))

    def test_exact_balance(self):
        self.assertTrue(can_transfer(Decimal("25.00"), Decimal("25.00")))

    def test_insufficient_balance(self):
        self.assertFalse(can_transfer(Decimal("10.00"), Decimal("20.00")))

    def test_zero_transfer(self):
        self.assertFalse(can_transfer(Decimal("50.00"), Decimal("0.00")))

    def test_negative_transfer(self):
        self.assertFalse(can_transfer(Decimal("50.00"), Decimal("-10.00")))

if __name__ == '__main__':
    unittest.main()
