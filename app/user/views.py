#-*- coding: utf-8 -*-                                                                                     

from flask import render_template, request, redirect, url_for, flash
from models import BookInfo, User
from models import SpiderForm, UserForm
from app import app
from . import user
from flask.ext.login import LoginManager
from flask.ext.login import login_user, logout_user, current_user, login_required

lm = LoginManager()
lm.init_app(app)

@lm.user_loader
def load_user(id):
    user = User.objects(id=id)
    if user:
        return user.first()
    else:
        return ''
    

@user.route('/Register')
def register():
    register_form = UserForm()
    return render_template('register.html', form=register_form)

@user.route('/handle_register', methods=['POST'])
def handle_register():
    register_form_info = UserForm(request.form)
    if register_form_info.validate():
        User(username=register_form_info.username.data, password=register_form_info.password.data,
             real_name=register_form_info.real_name.data).save()
        return 'Register done.'
    else:
        return 'Wrong!'

@user.route('/Login')
def login():
    login_form = UserForm()
    return render_template('login.html', form=login_form)

@user.route('/handle_login', methods=['POST'])
def handle_login():
    login_form_info = UserForm(request.form)
    if login_form_info.validate():
        username = login_form_info.username.data
        password = login_form_info.password.data
        user_online = User.objects(username=username, password=password)

        if user_online:
            print user_online.first().id
            login_user(user=user_online.first(), remember=True)
            print 'Login success'
            return redirect('/')
        else:
            return 'Login faild'
    else:
        print 'Wrong form'

@user.route('/handle_logout')
def handle_logout():
    logout_user()
    return redirect('/')

@user.route('/test_login')
@login_required
def test_login():
    print current_user.username
    return '~~~~'

