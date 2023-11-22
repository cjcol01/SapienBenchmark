from app import app
from flask import render_template

@app.route('/')
def home():
    return render_template('home.html')  

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

if __name__ == '__main__':
    app.run(debug=True)
