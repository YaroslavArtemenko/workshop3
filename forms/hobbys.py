from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField
from wtforms import validators


class HobbyForm(Form):

    hobby_name = StringField("Name: ", [
        validators.DataRequired("Please enter your  hobby name."),
        validators.Length(0,100, "Group name must be  include only 100 symbols")
    ])



    submit = SubmitField("Save")