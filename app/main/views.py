from flask import render_template,request,redirect,url_for,flash,abort
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
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@main.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@main.route('/post/<int:post_id>/update', methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post has been updated successfully!', 'success')
        return redirect(url_for('main.post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form,legend='Update Post')