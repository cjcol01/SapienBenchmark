# library imports
from flask import render_template, redirect, url_for, flash, session, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from . import app, db, bcrypt, login_manager
from datetime import datetime
from sqlalchemy.sql import func

# my file imports
from .models import User, PlaySession, Game, UserGame
from .forms import RegisterForm, LoginForm

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# home route, loads info from db and displays data
@app.route('/')
def home():
    # checks if user is logged in and sets data
    if current_user.is_authenticated:
        update_user_game()
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

        reaction_percentage = calculate_percentile(avg_reaction, GAME_ID_FOR_REACTION, 1)
        aim_percentage = calculate_percentile(avg_aim, GAME_ID_FOR_AIM, 2)
        typing_percentage = calculate_percentile(avg_typing, GAME_ID_FOR_TYPING, 3)
        verb_mem_percentage = calculate_percentile(avg_verbal_memory, GAME_ID_FOR_VERBAL_MEMORY, 4)

        # return all neccessary data 
        return render_template('home.html', username=username, 
        signup_date=signup_date, 
        avg_reaction=str(avg_reaction), reaction_percentage=reaction_percentage, 
        avg_aim=str(avg_aim), aim_percentage=aim_percentage,
        avg_typing=str(avg_typing), typing_percentage=typing_percentage,
        avg_verbal_memory=str(avg_verbal_memory), verb_mem_percentage=verb_mem_percentage, )

    else:
        # Handle guest or non-logged in users
        signup_date = datetime.now()
        return render_template('home.html', username="Guest", signup_date=signup_date, 
        avg_reaction=None, reaction_percentage="", 
        avg_aim=None, aim_percentage="",
        avg_typing=None, typing_percentage="",
        avg_verbal_memory=None, verb_mem_percentage="" )

# calculates what percentile the user falls in for various games
def calculate_percentile(user_score, game_id, game_id2):
    # Ensure user_score is an integer
    user_score = int(user_score)

    # Fetch the Game object
    game = Game.query.get(game_id2)
    if not game:
        return 0  # Return a default value if the game does not exist

    high_score_good = game.high_score_good

    # Get all scores for the game, convert them to integers, and handle empty strings
    all_scores = PlaySession.query.with_entities(PlaySession.score).filter_by(game_id=game_id).all()
    all_scores = [int(score[0]) if score[0] != '' else 0 for score in all_scores]

    if not all_scores:
        return 0  # In case there are no other scores

    # Count based on whether a high score is good or not
    if high_score_good:
        count_relevant = sum(score <= user_score for score in all_scores)
    else:
        count_relevant = sum(score >= user_score for score in all_scores)

    percentile = (count_relevant / len(all_scores)) * 100
    return round(percentile, 2)  # Rounded to two decimal places


# simple aimtrainer route 
@app.route('/aimtrainer')
def aim_trainer():
    return render_template('aimtrainer.html')

# simple reaction route 
@app.route('/reaction')
def reaction():
    return render_template('reaction.html')

# simple typing route 
@app.route('/typing')
def typing():
    return render_template('typing.html')

# simple verbal memory route 
@app.route('/verbalmemory')
def verbal_memory():
    return render_template('verbalmemory.html')

# login route, passes data to db for verification
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error_message = None

    # form submitted - query db
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("home"))
        else:
            error_message = 'Invalid email or password.'
    response = render_template("login.html", form=form, error_message=error_message)
    error_message = None
    return response

# simple logout method, returns to home page
@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("home"))

# signup page, passes client-side validated data to db for more validation check
@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please log in or use a different email.', 'error')
            return redirect(url_for('signup'))

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('signup'))

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for("login"))

    return render_template("signup.html", form=form)

@app.route('/check_email', methods=['POST'])
def check_email():
    email = request.form['email']
    user = User.query.filter_by(email=email).first()
    return jsonify({'isTaken': user is not None})


# move to config
GAME_ID_FOR_REACTION = "Reaction"


# submit reaction score to db
# probably a bad way of doing things
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


# submit aim score to db
# probably a bad way of doing things
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

# submit typing score to db
# probably a bad way of doing things
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

# submit verbmem score to db
# probably a bad way of doing things
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

# manage user session - not in use atm
@app.route('/user/<int:user_id>/sessions')
def user_sessions(user_id):
    # Query to fetch all play sessions with their related game for a specific user
    sessions = PlaySession.query.filter_by(user_id=user_id).join(Game).all()

    # You can now access game details in your template through each session
    return render_template('user_sessions.html', sessions=sessions)


# Function to update UserGame table
def update_user_game():
    # Calculate total plays and average score for each user-game combination
    play_data = db.session.query(
        PlaySession.user_id,
        PlaySession.game_id,
        func.count(PlaySession.id).label('total_plays'),
        func.avg(PlaySession.score).label('average_score')
    ).group_by(PlaySession.user_id, PlaySession.game_id).all()

    for data in play_data:
        user_id, game_id, total_plays, average_score = data

        # Check if record exists in UserGame
        user_game = UserGame.query.filter_by(user_id=user_id, game_id=game_id).first()

        if user_game:
            # Update existing record
            user_game.total_plays = total_plays
            user_game.average_score = average_score
        else:
            # Create new record and add to session
            new_user_game = UserGame(
                user_id=user_id,
                game_id=game_id,
                total_plays=total_plays,
                average_score=average_score
            )
            db.session.add(new_user_game)
    
    # Commit changes to the database
    db.session.commit()


# Run the application
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
