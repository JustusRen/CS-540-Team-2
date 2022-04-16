from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Movie, Rating
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

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    with Session(engine) as session:
        movie = session.query(Movie).order_by(func.rand()).first()
        if request.method == 'POST':
            rating = request.form.get('rating')
            new_rating = Rating(user_id=current_user.id, movie_id=movie.id, rating=rating)
            db.session.add(new_rating)
            db.session.commit()
            flash('New rating inserted!', category='success')
            return redirect(url_for('views.home'))
                
        return render_template("home.html", user=current_user, movie=movie)