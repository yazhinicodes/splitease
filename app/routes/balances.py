from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import GroupMember, Expense, ExpenseSplit

balances_bp = Blueprint('balances', __name__)

@balances_bp.route('/<int:group_id>/balances', methods=['GET'])
@jwt_required()
def get_balances(group_id):
    user_id = int(get_jwt_identity())

    member = GroupMember.query.filter_by(
        group_id=group_id, user_id=user_id
    ).first()
    if not member:
        return jsonify({'error' : 'You are not a member of this group'}), 403
    
    members = GroupMember.query.filter_by(group_id=group_id).all()
    member_ids = [m.user_id for m in members]

    net = {mid: 0.0 for mid in member_ids}

    expenses = Expense.query.filter_by(group_id=group_id).all()
    for expense in expenses:
        net[expense.paid_by] += expense.amount
        splits = ExpenseSplit.query.filter_by(expense_id=expense.id).all()
        for split in splits:
            net[split.user_id] -= split.share_amount

    transactions = settle(net)

    return jsonify({
        'balances' : net,
        'transactions' : transactions
    }), 200

def settle(net):
    creditors = []
    debtors = []

    for user_id, amount in net.items():
        if amount > 0.01:
            creditors.append([user_id, round(amount, 2)])
        elif amount < -0.01:
            debtors.append([user_id, round(abs(amount), 2)])

    creditors.sort(key=lambda x: x[1], reverse=True)
    debtors.sort(key=lambda x: x[1], reverse=True)
   
    transactions = []

    while creditors and debtors:
        creditor = creditors[0]
        debtor = debtors[0]

        settlement = min(creditor[1], debtor[1])
        settlement = round(settlement, 2)

        transactions.append({
            'from' : debtor[0],
            'to' : creditor[0],
            'amount' : settlement
        })

        creditor[1] = round(creditor[1] - settlement, 2)
        debtor[1] = round(debtor[1] - settlement, 2)

        if creditor[1] < 0.01:
            creditors.pop(0)
        if debtor[1] < 0.01:
            debtors.pop(0)

    return transactions
