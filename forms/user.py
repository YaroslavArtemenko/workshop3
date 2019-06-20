from flask_wtf import Form
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField
from wtforms import validators
from wtforms.fields.html5 import EmailField


class UserForm(Form):



   user_name = StringField("Name: ",[
                                    validators.DataRequired("Please enter your name."),
                                    validators.Length(3, 20, "Name should be from 3 to 20 symbols")
                                 ])


   user_email = EmailField("Email",  [
                                        validators.DataRequired("Please enter your email address."),
                                        validators.Email("Please enter your email address.")
                                    ])

   user_phone = StringField("phone: ",[
                                    validators.DataRequired("Please enter your phone."),
                                    validators.Length(0, 15, "phone should be 15 symbols")
                                 ])





   submit = SubmitField("Save")
