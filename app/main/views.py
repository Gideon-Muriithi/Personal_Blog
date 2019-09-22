from flask import render_template,request,redirect,url_for,flash
from . import main
from ..models import User,Post
from .. import db,photos
from .forms import PostForm
from flask_login import login_required,current_user
import datetime

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

@main.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        flash('Post created successfully!', 'success')
        return redirect(url_for('.index'))
    return render_template('create_post.html', title='New Post', form=form)
