from wtforms import Form, StringField, PasswordField, validators, IntegerField


class UserLoginForm(Form):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=1, max=25)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=1, max=200)])
