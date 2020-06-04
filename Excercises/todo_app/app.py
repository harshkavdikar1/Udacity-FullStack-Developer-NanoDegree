from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create an application with same name as name of the module
app = Flask(__name__)

# Config the URI of the postgres database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://student:student@localhost:5432/studentdb'

# Create a database object which links SQLAlchemy to our current app
db = SQLAlchemy(app)

# Configure database with current applcation for migrations
migrate = Migrate(app, db)

# Model the todo class


class Todo(db.Model):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    # Format the objects while printing
    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


# Need to comment it out when implementiong migrations
# Create model of all the classes in database
# db.create_all()


@app.route("/todos/create", methods=["POST"])
def create_todo():
    desc = request.get_json()["description"]
    # Create an object ot Todo
    todo = Todo(description=desc)
    # Add data to the table
    db.session.add(todo)
    # Flush the data and commit it to database
    db.session.commit()
    # should match the method name of the url
    return jsonify({
        "description": todo.description
    })


# Route the index page of the website to this method
@app.route("/index")
def index():
    # Flask will look for this file in templates folder
    # Todo.query.all() will all the records from table representing model Todo
    return render_template("index.html", data=Todo.query.order_by('id').all())


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        # Read checked or unchecked item from the client
        completed = request.get_json()['completed']
        # Get the element from back-end by querying by id
        todo = Todo.query.get(todo_id)
        # Update the model with checked value
        todo.completed = completed
        # Commit the changes to the database
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
  try:
    Todo.query.filter_by(id=todo_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({ 'success': True })

if __name__ == '__main__':
    app.run(debug=True)
