from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField, IntegerField
from wtforms import validators
from wtforms.fields.html5 import EmailField

class UserHobbyForm(Form):

    hobby_name = StringField("Name hobby: ", [
        validators.DataRequired("Please enter your  hobby name."),
        validators.Length(0, 100, "Group name must be  include only 100 symbols")
    ])

    user_email = EmailField("Email: ", [
        validators.DataRequired("Please enter your email."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])



    submit = SubmitField("Save")