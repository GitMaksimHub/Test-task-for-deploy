from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
from flask_mysqldb import MySQL


app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'afina7878om7878' #Здесь пароль от phpMyAdmin
app.config['MYSQL_DB'] = 'users'
app.config["SECRET_KEY"] = 'asdfjklfgdashasdkfghjasdk'


mysql = MySQL(app)


@app.route("/insert", methods=['POST'])
def insert():
    if request.method == "POST":

        flash("Data inserted!")

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.connection.commit()


        if 'userLogged' in session:
            return redirect(url_for("mainpage", username=session['userLogged']))
        return redirect(url_for('mainpage'))

@app.route("/update", methods=["POST", "GET"])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']


        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE users
        SET name=%s,email=%s,phone=%s
        WHERE id=%s
        """, (name, email, phone, id_data))
        flash("Data updated!")
        mysql.connection.commit()


        if 'userLogged' in session:
            return redirect(url_for("mainpage", username=session['userLogged']))
        return redirect(url_for('mainpage'))



@app.route('/delete/<string:id_data>', methods=["POST", "GET"])
def delete(id_data):
    flash("Deleted!")

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id=%s ", (id_data,))
    mysql.connection.commit()

    if 'userLogged' in session:
        return redirect(url_for("mainpage", username=session['userLogged']))
    return redirect(url_for('mainpage'))


@app.route("/mainpage/<username>")
def mainpage(username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users ")
    data = cur.fetchall()
    cur.close()


    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return render_template('mainpage.html', users = data)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        if len(request.form["password"]) < 8:
            flash("Length of password must been more than 8")
        else:
            flash("email: admin, password:1234")


    if 'userLogged' in session:
        return redirect(url_for("mainpage", username=session['userLogged']))

    elif request.form.get("username") == "admin" and request.form.get("password") == '1234':
        session['userLogged'] = request.form.get("username", "my default")
        return redirect(url_for('mainpage', username=session['userLogged']))

    return render_template('index.html')







#@app.errorhandler(404)
#def error_404(error):
#    return render_template('error404.html')

if __name__ == '__main__':
    app.run(debug=False)