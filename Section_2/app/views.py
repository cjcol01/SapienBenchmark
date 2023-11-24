from flask import render_template, redirect, url_for, flash, session
from . import app, db, bcrypt, login_manager
from .models import User
from .forms import RegisterForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    username = current_user.username if current_user.is_authenticated else "guest"
    signup_date = current_user.signup_date
    return render_template('home.html', username=username, signup_date=signup_date)


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

# Run the application
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
