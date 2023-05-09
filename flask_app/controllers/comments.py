from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.comment import Comment

@app.route('/make-comment', methods=['POST'])
def comment():
    # if not Comment.validate_comment(request.form):
    #     return redirect('/wall')
    data = {
    "content": request.form["comment"],
    "users_id": session['user_id'],
    "posts_id": request.form["post_id"]
    }
    post_id = Comment.save(data)
    return redirect('/wall')

