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

        # calculate the average score for reaction game
        avg_score_reaction_query = db.session.query(db.func.avg(PlaySession.score)).filter(
            PlaySession.user_id == current_user.id,
            PlaySession.game_id == GAME_ID_FOR_REACTION
        )
        avg_reaction = avg_score_reaction_query.scalar() or 0
        avg_reaction = int(round(avg_reaction))

        # calculate the average score for aim trainer game
        avg_score_aim_query = db.session.query(db.func.avg(PlaySession.score)).filter(
            PlaySession.user_id == current_user.id,
            PlaySession.game_id == GAME_ID_FOR_AIM
        )
        avg_aim = avg_score_aim_query.scalar() or 0
        avg_aim = int(round(avg_aim))

        # calculate the average score for typing game
        avg_score_typing_query = db.session.query(db.func.avg(PlaySession.score)).filter(
            PlaySession.user_id == current_user.id,
            PlaySession.game_id == GAME_ID_FOR_TYPING
        )
        avg_typing = avg_score_typing_query.scalar() or 0
        avg_typing = int(round(avg_typing))

        # calculate the average score for verbal memory game
        avg_score_verbal_memory_query = db.session.query(db.func.avg(PlaySession.score)).filter(
            PlaySession.user_id == current_user.id,
            PlaySession.game_id == GAME_ID_FOR_VERBAL_MEMORY
        )
        avg_verbal_memory = avg_score_verbal_memory_query.scalar() or 0
        avg_verbal_memory = int(round(avg_verbal_memory))

        reaction_percentage = 50
        aim_percentage = 60
        typing_percentage = 70
        verb_mem_percentage = 80

        return render_template('home.html', username=username, 
        signup_date=signup_date, 
        avg_reaction=str(avg_reaction), reaction_percentage=reaction_percentage, 
        avg_aim=str(avg_aim), aim_percentage=aim_percentage,
        avg_typing=str(avg_typing), typing_percentage=typing_percentage,
        avg_verbal_memory=str(avg_verbal_memory), verb_mem_percentage=verb_mem_percentage, )

    else:
        # Handle guest or non-logged in users
        signup_date = datetime.now()
        return render_template('home.html', username="guest", signup_date=signup_date, 
        avg_reaction=None, reaction_percentage=None, 
        avg_aim=None, aim_percentage=None,
        avg_typing=None, typing_percentage=None,
        avg_verbal_memory=None, verb_mem_percentage=None )



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
GAME_ID_FOR_REACTION = "Reaction"
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

GAME_ID_FOR_AIM = "Aim"
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

GAME_ID_FOR_TYPING = "Typing"
@app.route('/submit_typing_score', methods=['POST'])
def submit_typing_score():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    score = request.form.get('score')
    print("Typing Score is", score)

    play_session = PlaySession(user_id=current_user.id, game_id=GAME_ID_FOR_TYPING, score=score, date_played=datetime.utcnow())
    db.session.add(play_session)
    db.session.commit()

    return redirect(url_for('home'))

GAME_ID_FOR_VERBAL_MEMORY = "Verb mem"
@app.route('/submit_verbal_memory_score', methods=['POST'])
def submit_verbal_memory_score():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    score = request.form.get('score')
    print("Verbal Memory Score is", score)

    # Save the score to the database
    play_session = PlaySession(user_id=current_user.id, game_id=GAME_ID_FOR_VERBAL_MEMORY, score=score, date_played=datetime.utcnow())
    db.session.add(play_session)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/user/<int:user_id>/sessions')
def user_sessions(user_id):
    # Query to fetch all play sessions with their related game for a specific user
    sessions = PlaySession.query.filter_by(user_id=user_id).join(Game).all()

    # You can now access game details in your template through each session
    return render_template('user_sessions.html', sessions=sessions)

# Run the application
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
