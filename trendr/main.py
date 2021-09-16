from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import logout_user, current_user, login_required
from .extensions import db
from .tasks import *
from .models import *

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    return render_template('example.html')