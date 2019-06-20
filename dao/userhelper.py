from dao.db import OracleDb


class UserHelper:

    def __init__(self):
        self.db = OracleDb()

    def getHobbyData(self, hobby_name=None):

        if hobby_name:
            hobby_name="'{0}'".format(hobby_name)
        else:
            hobby_name='null'

        query = "select * from table(orm_hobby.GetHobbyData({0}))".format(hobby_name)

        result = self.db.execute(query)
        return result.fetchall()




if __name__ == "__main__":

    helper = UserHelper()

    print(helper.getHobbyData())
    print(helper.getHobbyData())
