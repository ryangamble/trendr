from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, logout_user, current_user, login_user
from .models import *
from .extensions import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    pass

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
   pass

@auth.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
