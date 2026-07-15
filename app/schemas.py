from marshmallow import Schema, fields, validate

class SignupSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class GroupSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))

class AddMemberSchema(Schema):
    email = fields.Email(required=True)

class ExpenseSchema(Schema):
    description = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    split_type = fields.Str(load_default='equal', validate=validate.OneOf(['equal']))

