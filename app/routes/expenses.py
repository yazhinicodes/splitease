from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Expense, ExpenseSplit, GroupMember
from app.schemas import ExpenseSchema
from marshmallow import ValidationError

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/<int:group_id>/expenses', methods=['POST'])
@jwt_required()
def add_expense(group_id):
    user_id = int(get_jwt_identity())
    schema = ExpenseSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    description = data['description']
    amount = data['amount']
    split_type = data['split_type']

    if not description or not amount:
        return jsonify({'error' : 'Description and amount are required'}), 400
    
    members = GroupMember.query.filter_by(group_id=group_id).all()
    if not members:
        return jsonify({'error' : 'Group not found or has no members'}), 404
    
    member_ids = [m.user_id for m in members]
    if user_id not in member_ids:
        return jsonify({'error' : 'You are not a member of this group'}), 403
    
    expense = Expense(
        group_id=group_id,
        paid_by=user_id,
        amount=amount,
        description=description
    )
    db.session.add(expense)
    db.session.flush()

    if split_type == 'equal':
        share = round(amount / len(member_ids), 2)
        for mid in member_ids:
            split = ExpenseSplit(
                expense_id=expense.id,
                user_id=mid,
                share_amount=share
            )
            db.session.add(split)

    db.session.commit()

    return jsonify({
        'message' : 'Expense added',
        'expense_id' : expense.id,
        'split_among' : len(member_ids),
        'share_per_person' : round(amount / len(member_ids), 2)
    }), 201

@expenses_bp.route('/<int:group_id>/expenses', methods=['GET'])
@jwt_required()
def get_expenses(group_id):
    user_id = int(get_jwt_identity())

    member = GroupMember.query.filter_by(
        group_id=group_id, user_id=user_id
    ).first()
    if not member:
        return jsonify({'error' : 'You are not a member of this group'}), 403
    
    expenses = Expense.query.filter_by(group_id=group_id).all()

    result = []
    for e in expenses:
        result.append({
            'id' : e.id,
            'description' : e.description,
            'amount' : e.amount,
            'paid_by' : e.paid_by,
            'created_at' : str(e.created_at)
        })

    return jsonify(result), 200

    


    