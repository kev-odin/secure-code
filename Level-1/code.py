"""
////////////////////////////////////////////////////////////
///                                                      ///
///   0. tests.py is passing but the code is vulnerable  /// 
///   1. Review the code. Can you spot the bug?          ///
///   2. Fix the code but ensure that tests.py passes    ///
///   3. Run hack.py and if passing then CONGRATS!       ///
///   4. If stuck then read the hint                     ///
///   5. Compare your solution with solution.py          ///
///                                                      ///
////////////////////////////////////////////////////////////
"""
# Based on what I have read on Google and looking at the test cases in the hack.py
# We are going to need to add constraints to accepted values to prevent an underflow scenario
# Helpful: https://www.youtube.com/watch?v=sUTulh6qXxY

MAX_AMOUNT = 100_000  # Highest priced item
MAX_QUANTITY = 10_000  # Limit quantity
MAX_TOTAL = 1e6  # Absolute limit

from collections import namedtuple
from decimal import Decimal

Order = namedtuple("Order", "id, items")
Item = namedtuple("Item", "type, description, amount, quantity")


def validorder(order: Order):
    net = Decimal("0")

    for item in order.items:
        if item.type == "payment":
            if -1 * MAX_AMOUNT < item.amount < MAX_AMOUNT:
                net += Decimal(str(item.amount))
        elif item.type == "product":
            if 0 < item.quantity <= MAX_QUANTITY and 0 < item.amount <= MAX_AMOUNT:
                net -= Decimal(str(item.amount)) * item.quantity
            if not -1 * MAX_TOTAL < net < MAX_TOTAL:
                return "Your order was not completed due to an internal system error."
        else:
            return f"Invalid item type: {item.type}"

    if net != 0:
        return f"Order ID: {order.id} - Payment imbalance: ${net:.2f}"
    return f"Order ID: {order.id} - Full payment received!"


def exploit(n: int = 1050):
    """Memory overflow at 1022 iterations"""
    under = 1
    over = 1
    factor = 2

    for i in range(n):
        under = under / factor
        over = over * factor
        print(f"Current value: {i} | {under:.2g} | {over:.2g}")
