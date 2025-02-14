from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

admver = "1.5"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server-privileges.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Privileges(db.Model):
    __tablename__ = 'privileges'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    permissions = db.Column(db.String(255), nullable=True)
    color = db.Column(db.String(255), nullable=True)

    def __init__(self, name, description, permissions, color):
        self.name = name
        self.description = description
        self.permissions = permissions
        self.color = color

    def __repr__(self):
        return f'<Privileges {self.name}>'


@app.before_request
def setup_database():
    """
    Ця функція виконується перед першим запитом до сервера.
    Вона перевіряє, чи всі необхідні таблиці створені, і створює їх, якщо це потрібно.
    """
    db.create_all()
    print("Таблиці створено (за потреби).")


@app.route('/')
def main():
    return render_template("pages/mainpage.html")


@app.route('/privileges')
def privileges():
    privileges_list = Privileges.query.all()
    return render_template("pages/privileges.html", privileges=privileges_list)


@app.route('/admin/<string:psw>', methods=['GET', 'POST'])
def admin(psw):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        permissions = request.form['permissions']
        color = request.form['color']
        privilege = Privileges(name, description, permissions, color)
        db.session.add(privilege)
        db.session.commit()
        return redirect(url_for('privileges'))

    if request.method == 'GET' and psw != "0105":
        return render_template("root/fail.html")

    return render_template("pages/admin.html")

@app.route("/dev")
def docs():
    return  render_template("pages/dev.html")

@app.route("/admin", methods=["GET", "POST"])
def admin_page():
    if request.method == "POST":
        password = request.form["password"]
        return redirect(f"/admin/{password}")

    return render_template("pages/admin-login.html")

@app.route("/about")
def about():
    return render_template("pages/about.html")


if __name__ == '__main__':
    app.run(debug=True)
