from app import app
from flask import render_template

@app.route('/home')
def home():
    title = 'I am trying it'
    return render_template('base.html', title=title)