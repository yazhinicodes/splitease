from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Group, GroupMember, User
from app.schemas import GroupSchema, AddMemberSchema
from marshmallow import ValidationError

groups_bp = Blueprint('groups_by', __name__)

@groups_bp.route('', methods=['POST'])
@jwt_required()
def create_group():
    user_id = int(get_jwt_identity())
    schema = GroupSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    name = data['name']
    
    new_group = Group(name=name, created_by=user_id)
    db.session.add(new_group)
    db.session.flush()

    member = GroupMember(group_id=new_group.id, user_id=user_id)
    db.session.add(member)
    db.session.commit()

    return jsonify({'message' : 'Group created', 'group_id' : new_group.id}), 201


@groups_bp.route('', methods=['GET'])
@jwt_required()
def get_my_groups():
    user_id = int(get_jwt_identity())

    memberships = GroupMember.query.filter_by(user_id=user_id).all()
    group_ids = [m.group_id for m in memberships]
    groups = Group.query.filter(Group.id.in_(group_ids)).all()

    result = [{'id' : g.id, 'name' : g.name, 'created_by' : g.created_by}for g in groups]
    return jsonify(result), 200

@groups_bp.route('/<int:group_id>/members', methods=['POST'])
@jwt_required()
def add_member(group_id):
    user_id = int(get_jwt_identity())
    schema = AddMemberSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    new_member_email = data['email']

    group = Group.query.get(group_id)
    if not group:
        return jsonify({'error': 'Group not found'}), 404

    if group.created_by != user_id:
        return jsonify({'error': 'Only the group creator can add members'}), 403

    new_member = User.query.filter_by(email=new_member_email).first()
    if not new_member:
        return jsonify({'error': 'User not found'}), 404

    already_member = GroupMember.query.filter_by(
        group_id=group_id, user_id=new_member.id
    ).first()
    if already_member:
        return jsonify({'error': 'User already in group'}), 409

    member = GroupMember(group_id=group_id, user_id=new_member.id)
    db.session.add(member)
    db.session.commit()

    return jsonify({'message': f'{new_member.name} added to group'}), 201