from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Movie, Rating, Recommendation
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import func
from  sqlalchemy.sql.expression import func, select
from sqlalchemy import create_engine,  or_
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
        
        try:
            rec = session.query(Recommendation).filter_by(user_id = current_user.id).first()
            rec1_movie_name = session.query(Movie).filter_by(id = rec.rec1).first()
            rec2_movie_name = session.query(Movie).filter_by(id = rec.rec2).first()
            rec3_movie_name = session.query(Movie).filter_by(id = rec.rec3).first()
            
            try:
                buddy1_rec = session.query(Recommendation).filter(Recommendation.user_id != current_user.id).filter(or_(Recommendation.rec1 == rec.rec1, Recommendation.rec2 == rec.rec1, Recommendation.rec3 == rec.rec1, Recommendation.rec1 == rec.rec2, Recommendation.rec2 == rec.rec2, Recommendation.rec3 == rec.rec2, Recommendation.rec1 == rec.rec3, Recommendation.rec2 == rec.rec3, Recommendation.rec3 == rec.rec3)).first()
                #buddy2_rec = session.query(Recommendation).filter(Recommendation.user_id != current_user.id).filter(or_(Recommendation.rec1 == rec.rec2, Recommendation.rec2 == rec.rec2, Recommendation.rec3 == rec.rec2)).first()
                #buddy3_rec = session.query(Recommendation).filter(Recommendation.user_id != current_user.id).filter(or_(Recommendation.rec1 == rec.rec3, Recommendation.rec2 == rec.rec3, Recommendation.rec3 == rec.rec3)).first()
                #print(buddy2_rec.user_id)
                #print(buddy3_rec.user_id)

                buddy1_user = session.query(User).filter_by(id = buddy1_rec.user_id).first()
                #buddy2_user = session.query(User).filter_by(id = buddy2_rec.user_id).first()
                #buddy3_user = session.query(User).filter_by(id = buddy3_rec.user_id).first()
                return render_template("home.html", user=current_user, movie=movie, rec1=rec1_movie_name.title, rec2=rec2_movie_name.title, rec3=rec3_movie_name.title, buddy1=buddy1_user.first_name)
            except:
                return render_template("home.html", user=current_user, movie=movie, rec1=rec1_movie_name.title, rec2=rec2_movie_name.title, rec3=rec3_movie_name.title, buddy1="Rate movies to find buddies")
        except:
            return render_template("home.html", user=current_user, movie=movie, rec1="Rate movies to get recommendations", rec2="Rate movies to get recommendations", rec3="Rate movies to get recommendations", buddy1="Rate movies to find buddies")

