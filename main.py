import datetime

from flask import Flask, request, render_template, redirect, url_for
from sqlalchemy import func, text

from dao.db import OracleDb
from dao.orm.model import ormUser, ormHobby, ormUserHobby
from sqlalchemy.sql import func
from forms.hobbys import HobbyForm
from forms.user import UserForm
from forms.userhobby import UserHobbyForm
from forms.searchForm import SearchForm
from forms.SearchForm1 import SearchForm1



app = Flask(__name__)
app.secret_key = 'development key'
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

import json




@app.route('/', methods=['GET', 'POST'])
def root():

    return render_template('index.html')






@app.route('/search', methods=['GET', 'POST'])
def search():

    search_form = SearchForm()

    if request.method=='GET':
        return render_template('search.html', form = search_form, result=None)
    else:
        return render_template('search.html', form = search_form, result=search_form.get_result_by_Group())


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    db = OracleDb()



    query1 = (
        db.sqlalchemy_session.query(
            ormUser.user_name,
            func.count(ormUserHobby.hobby_name).label('hobby_count')
        ). \
            outerjoin(ormUserHobby).
 \
            group_by(ormUser.user_name)
    ).all()


    #select
    #count(user_name), hobby_name
    #from orm_user join orm_user_hobby
    #on orm_user.user_email = orm_user_hobby.user_email
    #group by(hobby_name)


    query2 = (
        db.sqlalchemy_session.query(
            ormHobby.hobby_name,
            func.count(ormUserHobby.user_email).label('user_count')
        ). \
            outerjoin(ormUserHobby).
 \
            group_by(ormHobby.hobby_name)
    ).all()




    hobby_name, user_counts = zip(*query2)
    pie = go.Pie(
        labels=hobby_name,
        values=user_counts
    )

    names, hobby_counts = zip(*query1)
    bar = go.Bar(
        x=names,
        y=hobby_counts
    )



    data = {
                "bar":[bar],
                "pie":[pie]
           }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphsJSON=graphsJSON)

#     =================================================================================================


@app.route('/new_user', methods=['GET','POST'])
def new_user():

    form = UserForm()


    if request.method == 'POST':
        if form.validate() == False:
            return render_template('user.html', form=form, form_name="New user", action="new_user")
        else:
            new_user= ormUser(
                                user_name=form.user_name.data,
                                user_email=form.user_email.data,
                                user_phone=form.user_phone.data

                            )
            db = OracleDb()
            db.sqlalchemy_session.add(new_user)
            db.sqlalchemy_session.commit()


            return redirect(url_for('all_user'))

    return render_template('user.html', form=form, form_name="New user", action="new_user")



@app.route('/edit_user', methods=['GET','POST'])
def edit_user():

    form = UserForm()


    if request.method == 'GET':

        user_email =request.args.get('user_email')
        db = OracleDb()
        user = db.sqlalchemy_session.query(ormUser).filter(ormUser.user_email == user_email).one()

        # fill form and send to teacher
        form.user_email.data=user.user_email
        form.user_name.data=user.user_name
        form.user_phone.data=user.user_phone

        return render_template('user.html', form=form, form_name="Edit user", action="edit_user")


    else:

        if form.validate() == False:
            return render_template('user.html', form=form, form_name="Edit user", action="edit_user")
        else:
            db = OracleDb()
            # find user
            user = db.sqlalchemy_session.query(ormUser).filter(ormUser.user_email == form.user_email.data).one()

            # update fields from form data
            user.user_email = form.user_email.data
            user.user_name = form.user_name.data
            user.user_phone = form.user_phone.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('all_user'))





@app.route('/delete_user', methods=['POST'])
def delete_user():

    user_email = request.form['user_email']

    db = OracleDb()

    result = db.sqlalchemy_session.query(ormUser).filter(ormUser.user_email == user_email).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()


    return user_email

@app.route('/new_hobby', methods=['GET','POST'])
def new_hobby():
    form = HobbyForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('hobby.html', form=form, form_name="New hobby", action="new_hobby")
        else:
            new_hobby = ormHobby(
                hobby_name=form.hobby_name.data,

            )
            db = OracleDb()
            db.sqlalchemy_session.add(new_hobby)
            db.sqlalchemy_session.commit()

            return redirect(url_for('all_hobby'))

    return render_template('hobby.html', form=form, form_name="New hobby", action="new_hobby")


@app.route('/edit_hobby', methods=['GET', 'POST'])
def edit_hobby():
    form = HobbyForm()

    if request.method == 'GET':

        hobby_name = request.args.get('hobby_name')
        db = OracleDb()
        hobby = db.sqlalchemy_session.query(ormHobby).filter(ormHobby.hobby_name == hobby_name).one()

        # fill form and send to hobby

        form.hobby_name.data = hobby.hobby_name


        return render_template('hobby.html', form=form, form_name="Edit hobby", action="edit_hobby")


    else:

        if form.validate() == False:
            return render_template('hobby.html', form=form, form_name="Edit hobby", action="edit_hobby")
        else:
            db = OracleDb()
            # find user
            hobby = db.sqlalchemy_session.query(ormHobby).filter(ormHobby.hobby_name == form.hobby_name.data).one()

            # update fields from form data

            hobby.hobby_name = form.hobby_name.data


            db.sqlalchemy_session.commit()

            return redirect(url_for('all_hobby'))


@app.route('/delete_hobby', methods=['POST'])
def delete_hobby():
    hobby_name = request.form['hobby_name']

    db = OracleDb()

    result = db.sqlalchemy_session.query(ormHobby).filter(ormHobby.hobby_name == hobby_name).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return hobby_name

@app.route('/new_userhobby', methods=['GET','POST'])
def new_userhobby():
    form = UserHobbyForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('userhobby.html', form=form, form_name="New userhobby", action="new_userhobby")
        else:
            new_userhobby = ormUserHobby(
                user_email=form.user_email.data,
                hobby_name=form.hobby_name.data,


            )
            db = OracleDb()
            db.sqlalchemy_session.add(new_userhobby)
            db.sqlalchemy_session.commit()

            return redirect(url_for('all_userhobby'))

    return render_template('userhobby.html', form=form, form_name="New userhobby", action="new_userhobby")


@app.route('/edit_userhobby', methods=['GET', 'POST'])
def edit_userhobby():
    form = UserHobbyForm()

    if request.method == 'GET':
        userhobby_name = request.args.get('userhobby_name')
        userhobby_email = request.args.get('userhobby_email')
        db = OracleDb()
        userhobby = db.sqlalchemy_session.query(ormUserHobby).filter(ormUserHobby.user_email == userhobby_email, ormUserHobby.hobby_name == userhobby_name).one()

        # fill form and send to user

        form.user_email.data = userhobby.user_email
        form.hobby_name.data = userhobby.hobby_name

        return render_template('userhobby_form.html', form=form, form_name="Edit userhobby", action="edit_userhobby")

    else:

        if form.validate() == False:
            return render_template('userhobby_form.html', form=form, form_name="Edit userhobby", action="edit_userhobby")
        else:
            db = OracleDb()
            # find user
            uh = db.sqlalchemy_session.query(ormUserHobby).filter(ormUserHobby.user_email == form.user_email.data, ormUserHobby.hobby_name == form.hobby_name.data).one()

            # update fields from form data

            uh.user_email = form.user_email.data
            uh.hobby_name = form.hobby_name.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('userhobby'))


@app.route('/delete_userhobby', methods=['POST'])
def delete_userhobby():
    userhobby_email = request.form['userhobby_email']
    userhobby_name = request.form['userhobby_name']

    db = OracleDb()

    result = db.sqlalchemy_session.query(ormUserHobby).filter(ormUserHobby.user_email == userhobby_email, ormUserHobby.hobby_name == userhobby_name).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return userhobby_email, userhobby_name

@app.route('/searchuser', methods=['GET', 'POST'])

def searchUser():

     search_form = SearchForm()

     if request.method=='GET':
        #search_form.user_email.label='user email:'
        return render_template('search.html', form = search_form, result=None , action ='searchUser',name = 'User')
     else:
        #search_form.user_email.label = 'user email:'
        return render_template('search.html', form = search_form, result=search_form.get_result_Email()
                               , action ='searchUser',name = 'user')
@app.route('/searchhobby', methods=['GET', 'POST'])
def searchHobby():

     search_form = SearchForm1()

     if request.method=='GET':
        #search_form.hobby_name.label='Hobby name:'
        return render_template('search1.html', form = search_form, result=None , action ='searchHobby',name = 'Hobby')
     else:
        #search_form.hobby_name.label = 'Hobby name:'
        return render_template('search1.html', form = search_form, result=search_form.get_result_Hobby(), action ='searcHobby',name = 'Hobby')

@app.route('/all_user', methods=['GET'])
def all_user():
    db = OracleDb()

    result = db.sqlalchemy_session.query(ormUser).all()


    print(result)
    return render_template('all_user.html', result=result)

@app.route('/all_hobby', methods=['GET'])
def all_hobby():
    db = OracleDb()

    result = db.sqlalchemy_session.query(ormHobby).all()


    print(result)
    return render_template('all_hobby.html', result=result)

@app.route('/all_userhobby', methods=['GET'])
def all_userhobby():
    db = OracleDb()

    result = db.sqlalchemy_session.query(ormUserHobby).all()


    print(result)
    return render_template('all_userhobby.html', result=result)


if __name__ == '__main__':
    app.run(debug=True, port = 5001)