from flask import Flask, render_template
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


# Route the home page of the website to this decorator
@app.route("/")
def index():
    # Flask will look for this file in templates folder
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)