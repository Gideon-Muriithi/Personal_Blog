from flask import render_template
from . import main

posts = [
    {
        'author': 'Gideon M.',
        'title': 'Blog Post',
        'content': 'First Post',
        'date_posted': 'July 1, 2019',
    },

    {
        'author': 'Jane Doe',
        'title': 'Blog Post 1',
        'content': 'Second Post',
        'date_posted': 'June  21, 2019',
    }
]

@main.route('/')
def index():
    return render_template('index.html', posts=posts)

@main.route('/about')
def about():
    return render_template('about.html', title='About')

@main.route('/post/new')
@login_required
def new_post():
    return render_template('create_post.html', title='New Post')
