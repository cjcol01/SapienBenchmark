from flask import render_template, redirect, url_for, flash, session, request
from . import app, db, bcrypt, login_manager
from .models import User, PlaySession, Game, UserGame
from .forms import RegisterForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    if current_user.is_authenticated:
        username = current_user.username
        signup_date = current_user.signup_date

        # Query to calculate the average score for the reaction game
        avg_score_reaction_query = db.session.query(db.func.avg(PlaySession.score)).filter(
            PlaySession.user_id == current_user.id,
            PlaySession.game_id == GAME_ID_FOR_REACTION
        )
        avg_reaction = avg_score_reaction_query.scalar() or 0
        avg_reaction = int(round(avg_reaction))

        # Query to calculate the average score for the aim trainer game
        avg_score_aim_query = db.session.query(db.func.avg(PlaySession.score)).filter(
            PlaySession.user_id == current_user.id,
            PlaySession.game_id == GAME_ID_FOR_AIM
        )
        avg_aim = avg_score_aim_query.scalar() or 0
        avg_aim = int(round(avg_aim))

        return render_template('home.html', username=username, signup_date=signup_date, avg_score_reaction=avg_reaction, avg_score_aim=avg_aim)

    else:
        # Handle guest or non-logged in users
        return render_template('home.html', username="guest", signup_date=None, avg_score_reaction=None, avg_score_aim=None)


@app.route('/aimtrainer')
def aim_trainer():
    return render_template('aimtrainer.html')

@app.route('/reaction')
def reaction():
    return render_template('reaction.html')

@app.route('/typing')
def typing():
    return render_template('typing.html')

@app.route('/verbalmemory')
def verbal_memory():
    return render_template('verbalmemory.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("home"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Include email data from the form
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)

# move to config
GAME_ID_FOR_REACTION = 1

@app.route('/submit_reaction_score', methods=['POST'])
def submit_reaction_score():
    if not current_user.is_authenticated:
        flash("You need to be logged in to save your score.", "warning")
        return redirect(url_for('login'))

    score = request.form.get('score')
    # Validate and process the score, update the database, etc.

    play_session = PlaySession(user_id=current_user.id, game_id=GAME_ID_FOR_REACTION, score=score, date_played=datetime.utcnow())
    db.session.add(play_session)
    db.session.commit()

    flash("Score saved successfully!", "success")
    return redirect(url_for('home'))

GAME_ID_FOR_AIM = 2
@app.route('/submit_aim_score', methods=['POST'])
def submit_aim_score():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    score = request.form.get('score')
    print("Score is", score)

    # Validate and process the score, update the database, etc.
    play_session = PlaySession(user_id=current_user.id, game_id=GAME_ID_FOR_AIM, score=score, date_played=datetime.utcnow())
    db.session.add(play_session)
    db.session.commit()

    return redirect(url_for('home'))



# Run the application
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
