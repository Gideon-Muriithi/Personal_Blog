from flask import render_template,request,redirect,url_for,flash
from . import main
from ..models import User,Post
from .. import db,photos
from .forms import PostForm
from flask_login import login_required,current_user
import datetime


@main.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@main.route('/about')
def about():
    return render_template('about.html', title='About')

@main.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('.index'))
    return render_template('create_post.html', title='New Post', form=form)
