from flask import Blueprint, render_template , request , flash ,redirect, url_for
from flask_login import login_required, current_user 
from .models import Post , User , Comment
from .scrap import news_scrapper
views = Blueprint("views", __name__)
from . import db

@views.route("/")
@login_required
def home():
    return render_template("home.html")

@views.route("/createpost", methods=['GET', 'POST'])
@login_required
def createpost():
    if request.method == "POST":
        content = request.form.get('content')
        # print(content, current_user.username)

        if  not content :
            flash("post cannot be empty" , category="error")
            
        else:
            post = Post( text = content ,  author = current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("post created" , category='success')
            return redirect(url_for('views.home'))

    return render_template('createpost.html', user=current_user)

@views.route("/profile/<username>" )
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    # print(user)
    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))
    posts = Post.query.all()
    # for post in posts:
    #     print(post.text)
    return render_template('profile.html', user=current_user, posts=posts, username=username)

@views.route("/delete-post/<id>")
@login_required
def deletepost(id):
    post = Post.query.filter_by(id = id).first()

    if not post:
        flash("Post doesnot exist", category='error')
        print("not exist")
    elif current_user.id != post.author :
        print("yaha")
        flash("you do not have permission" , category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        print("deleted success")
        flash('post deleted' , category='success')

    return redirect(url_for('views.home'))

@views.route("/create-comment/<post_id>" , methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash("comment cannot be empty" , category='error')
    else:
        post = Post.query.filter_by(id = post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id = post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('post does not exist', category='error')

    return redirect(url_for('views.home'))

@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))

@views.route("/latest-news" , methods= ['GET'])
def news_scrap():
    content = news_scrapper()
    return render_template("scrap.html" , content = content)