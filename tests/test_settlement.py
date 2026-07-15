import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.routes.balances import settle

def test_no_debts():
    net = {1: 0.0, 2: 0.0, 3: 0.0}
    result = settle(net)
    assert result == []

def test_simple_two_person():
    net = {1: 500.0, 2: -500.0}
    result = settle(net)
    assert len(result) == 1
    assert result[0]['from'] == 2
    assert result[0]['to'] == 1
    assert result[0]['amount'] == 500.0

def test_three_person_equal():
    net = {1: 200.0, 2: -100.0, 3: -100.0}
    result = settle(net)
    assert len(result) == 2
    total_settled = sum(t['amount'] for t in result)
    assert round(total_settled, 2) == 200.0

def test_one_creditor_two_debtors_unequal():
    net = {1: 900.0, 2: -600.0, 3: -300.0}
    result = settle(net)
    assert len(result) == 2
    assert all(t['to'] == 1 for t in result)
    total = sum(t['amount'] for t in result)
    assert round(total, 2) == 900.0

def test_balances_sum_to_zero():
    net = {1: 300.0, 2: -150.0, 3: -150.0}
    result = settle(net)
    total_in = sum(t['amount'] for t in result if t['to'] == 1)
    assert round(total_in, 2) == 300.0