from flask import render_template, redirect,url_for,abort,request
from . import main
from app.requests import get_quote
from flask_login import login_required,current_user
from ..models import User,Blog,Comment,Subscriber
from ..import db, photos
import secrets
import os
from PIL import Image
from .forms import UpdateProfile,CreateBlog
from ..email import mail_message



#Views
@main.route('/')
def index():
    quote = get_quote()
    blogs = Blog.query.order_by(Blog.time.desc())
    return render_template('index.html', blogs=blogs,quote = quote)

@main.route('/profile/<name>',methods = ['POST','GET'])
@login_required
def profile(name):
    user = User.query.filter_by(username = name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()

    return render_template('profile/profile.html',user = user)

@main.route('/user/<name>/updateprofile', methods = ['POST','GET'])
@login_required
def updateprofile(name):
    user = User.query.filter_by(username = name).first()
    form = UpdateProfile()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.bio = form.bio.data
        db.session.commit()
        return redirect(url_for('main.profile',name=user.username,))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    return render_template('profile/update.html', user = user, form =form)

@main.route('/new_post', methods=['POST','GET'])
@login_required
def new_blog():
    subscribers = Subscriber.query.all()
    form = CreateBlog()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        content = form.content.data
        user_id =  current_user._get_current_object().id
        blog = Blog(title=title,description = description, content=content,user_id=user_id)
        blog.save()
        for subscriber in subscribers:
            mail_message("New Blog Post","email/new_blog",subscriber.email,blog=blog)
        return redirect(url_for('main.index'))
    return render_template('post.html', form = form)

@main.route('/blog/<id>')
@login_required
def blog(id):
    comments = Comment.query.filter_by(blog_id=id).all()
    blog = Blog.query.get(id)
    return render_template('blog_page.html',blog=blog,comments=comments)
    

@main.route('/blog/<blog_id>/update', methods = ['GET','POST'])
@login_required
def updateblog(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    form = CreateBlog()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.description = form.description.data
        blog.content = form.content.data
        db.session.commit()
        return redirect(url_for('main.blog',id = blog.id)) 
    if request.method == 'GET':
        form.title.data = blog.title
        form.description.data = blog.description
        form.content.data = blog.content
    return render_template('edit_blog.html', form = form)



@main.route('/comment/<blog_id>', methods = ['Post','GET'])
@login_required
def comment(blog_id):
    blog = Blog.query.get(blog_id)
    comment =request.form.get('newcomment')
    new_comment = Comment(comment = comment, user_id = current_user._get_current_object().id, blog_id=blog_id)
    new_comment.save()
    return redirect(url_for('main.blog',id = blog.id))

@main.route('/subscribe',methods = ['POST','GET'])
def subscribe():
    email = request.form.get('subscriber')
    new_subscriber = Subscriber(email = email)
    new_subscriber.save_subscriber()


    return redirect(url_for('main.index'))

@main.route('/blog/<blog_id>/delete', methods = ['POST'])
@login_required
def delete_post(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    blog.delete()
    return redirect(url_for('main.index'))

@main.route("/blog/<int:id>/<int:comment_id>/delete")
@login_required
def delete_comment(id, comment_id):
    blog = Blog.query.filter_by(id = id).first()
    comment = Comment.query.filter_by(id = comment_id).first()
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('main.blog',id = blog.id))

@main.route('/user/<string:username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first()
    blogs = Blog.query.filter_by(user=user).order_by(Blog.time.desc())
    return render_template('user.html',blogs=blogs,user = user)
