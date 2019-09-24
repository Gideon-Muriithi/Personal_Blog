from flask import render_template,request,redirect,url_for,flash,abort
from . import main
from ..models import User,Post
from .. import db,photos
from .forms import PostForm, CommentForm
from flask_login import login_required,current_user
import datetime
from ..requests import getQuotes


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    quote = getQuotes()
    return render_template('index.html', posts=posts, quote=quote)

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

# @main.route('/post/<int:post_id>/comment', methods=['GET','POST'])
# def comment(post_id):
#     post = Post.query.get_or_404(post_id)
#      form = CommentForm()
    
#     return render_template('comments.html')


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

@main.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted!', 'success')
    return redirect(url_for('.index'))

@main.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=2)
    return render_template('user_posts.html', posts=posts, user=user)