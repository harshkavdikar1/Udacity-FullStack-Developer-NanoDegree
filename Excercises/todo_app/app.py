from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create an application with same name as name of the module
app = Flask(__name__)

# Config the URI of the postgres database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://student:student@localhost:5432/studentdb'

# Create a database object which links SQLAlchemy to our current app
db = SQLAlchemy(app)

# Model the todo class


class Todo(db.Model):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    # Format the objects while printing
    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


# Create model of todo class in database
db.create_all()


@app.route("/create", methods=["POST"])
def create_todo():
    desc = request.form.get("description", "")
    # Create an object ot Todo
    todo = Todo(description=desc)
    # Add data to the table
    db.session.add(todo)
    # Flush the data and commit it to database
    db.session.commit()
    # should match the method name of the url
    return redirect(url_for("index"))


# Route the index page of the website to this method
@app.route("/index")
def index():
    # Flask will look for this file in templates folder
    # Todo.query.all() will all the records from table representing model Todo
    return render_template("index.html", data=Todo.query.all())


if __name__ == '__main__':
    app.run(debug=True)
