from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
    "first_name": request.form["first_name"],
    "last_name" : request.form["last_name"],
    "email" : request.form["email"],
    "password" : pw_hash,
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/wall')

@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash("A user with this email address does not exist. Please register first.", 'login')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Password", 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['user_name'] = user_in_db.first_name
    return redirect("/wall")

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')


# @app.route('/orders/getone/<int:order_id>')
# def getone(order_id):
#     order = Order.get_one(order_id)
#     return render_template("readone.html", order=order)

# @app.route('/cookies/edit/<int:order_id>')
# def editform(order_id):
#     order = Order.get_one(order_id)
#     return render_template("edit.html", order=order)


# @app.route('/cookies/edit', methods=['POST'])
# def update():
#     if not Order.validate_order(request.form):
#         redirect_route = '/cookies/edit/' + request.form["id"]
#         return redirect(redirect_route)
#     order_id = request.form["id"]
#     Order.update(request.form)
#     return redirect('/cookies')


# @app.route('/orders/delete/<int:order_id>')
# def delete(order_id):
#     Order.delete(order_id)
#     return redirect('/')