from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.post import Post

@app.route('/make-post', methods=['POST'])
def post():
    if not Post.validate_post(request.form):
        return redirect('/wall')
    data = {
    "content": request.form["post"],
    "users_id": session['user_id']
    }
    post_id = Post.save(data)
    return redirect('/wall')

@app.route('/wall')
def wall():   
    if 'user_id' not in session:
        return redirect('/')
    all_the_posts = Post.get_all_posts()
    return render_template("wall.html", all_the_posts=all_the_posts)

@app.route('/posts/delete/<int:post_id>')
def delete(post_id):
    Post.delete(post_id)
    return redirect('/wall')
