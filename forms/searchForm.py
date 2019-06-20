from flask_wtf import Form
from wtforms import StringField, SubmitField

from dao.userhelper import UserHelper
from wtforms.fields.html5 import EmailField


class SearchForm(Form):
    user_email = EmailField('User email: ')
    submit = SubmitField('Search')


    def get_result_Email(self):
        helper = UserHelper()
        return helper.getVariable(self.user_email.data)
