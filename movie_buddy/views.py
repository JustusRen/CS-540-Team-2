from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Movie
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import func
from  sqlalchemy.sql.expression import func, select
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import config

engine = create_engine(f'mysql+pymysql://{config.DB_CONNECTION}', echo=False)


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    with Session(engine) as session:
        movie = session.query(Movie).order_by(func.rand()).first()
        print(movie)
        return render_template("home.html", user=current_user, movie=movie)