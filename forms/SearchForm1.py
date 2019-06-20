from flask_wtf import Form
from wtforms import StringField, SubmitField

from dao.userhelper import UserHelper


class SearchForm1(Form):
    hobby_name = StringField('Name hobby: ')
    submit = SubmitField('Search')

    def get_result_Hobby(self):
        helper = UserHelper()
        return helper.getHobbyData(self.hobby_name.data)