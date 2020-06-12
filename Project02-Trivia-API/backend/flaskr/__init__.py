import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS. Allow '*' for origins.
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        '''
        After_request decorator to set Access-Control-Allow
        '''
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type, Authorization")
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, DELETE")
        return response

    @app.route("/categories", methods=["GET"])
    def get_categories():
        '''
        The endpoint to handle GET requests 
        for all available categories.
        '''
        categories = dict()

        for category in Category.query.all():
            categories[category.id] = category.type

        return jsonify({
            "categories": categories,
            "success": True
        })

    @app.route("/questions", methods=["GET"])
    def get_questions():
        '''
        The endpoint to handle GET requests for questions, 
        including pagination (every 10 questions). 
        This endpoint should return a list of questions, 
        number of total questions, current category, categories. 

        TEST: At this point, when you start the application
        you should see questions and categories generated,
        ten questions per page and pagination at the bottom of the screen for three pages.
        Clicking on the page numbers should update the questions. 
        '''

        questions = list()

        categories = dict()

        for category in Category.query.all():
            categories[category.id] = category.type

        page = int(request.args.get("page", 1))

        start = (page-1)*10
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in Question.query.all()]

        return jsonify({
            "questions": questions[start:end],
            "success": True,
            "total_questions": len(questions),
            "categories": categories
        })

    @app.route("/questions/<question_id>", methods=['DELETE'])
    def delete_question(question_id):
        '''
        An endpoint to DELETE question using a question ID. 

        TEST: When you click the trash icon next to a question, the question will be removed.
        This removal will persist in the database and when you refresh the page. 
        '''

        try:
            question = Question.query.get(question_id)
            if not question:
                abort(422)
            question.delete()
        except:
            abort(500)

        return jsonify({
            "deleted": question_id,
            "success": True
        })

    @app.route("/questions", methods=["POST"])
    def add_question():
        '''
        The endpoint to POST a new question, 
        which will require the question and answer text, 
        category, and difficulty score.

        TEST: When you submit a question on the "Add" tab, 
        the form will clear and the question will appear at the end of the last page
        of the questions list in the "List" tab.  
        '''

        data = request.get_json()

        try:
            question = Question(data["question"], data["answer"],
                                data["category"], int(data["difficulty"]))

            question.insert()
        except:
            abort(500)

        return jsonify(question.format())

    @app.route("/search", methods=["POST"])
    def search_questions():
        '''
        A POST endpoint to get questions based on a search term. 
        It should return any questions for whom the search term 
        is a substring of the question. 

        TEST: Search by any phrase. The questions list will update to include 
        only question that include that string within their question. 
        Try using the word "title" to start. 
        '''

        if not request.json.get("searchTerm"):
            abort(404)

        categories = dict()

        for category in Category.query.all():
            categories[category.id] = category.type

        search_term = "%" + request.json.get("searchTerm", "") + "%"

        questions = Question.query.filter(Question.question.ilike(search_term))

        if not questions:
            abort(404)

        questions = [question.format() for question in questions]

        return jsonify({
            "questions": questions,
            "success": True,
            "total_questions": len(questions),
            "categories": categories
        })

    @app.route("/categories/<category_id>/questions", methods=["GET"])
    def get_questions_with_category(category_id):
        '''
        A GET endpoint to get questions based on category. 

        TEST: In the "List" tab / main screen, clicking on one of the 
        categories in the left column will cause only questions of that 
        category to be shown. 
        '''

        category_id = category_id

        questions = [question.format() for question in Question.query.filter_by(
            category=str(category_id))]

        current_category = Category.query.get(category_id)

        if not current_category or not questions:
            abort(404)

        return jsonify({
            "questions": questions,
            "success": True,
            "total_questions": len(questions),
            "current_category": current_category.type
        })

    @app.route("/quizzes", methods=["POST"])
    def get_quiz_questions():
        '''
        A POST endpoint to get questions to play the quiz. 
        This endpoint should take category and previous question parameters 
        and return a random questions within the given category, 
        if provided, and that is not one of the previous questions. 

        TEST: In the "Play" tab, after a user selects "All" or a category,
        one question at a time is displayed, the user is allowed to answer
        and shown whether they were correct or not. 
        '''

        quiz = request.get_json()["quiz_category"]

        if "id" not in quiz:
            abort(422)

        category_id = quiz["id"]

        previous_questions = request.get_json()["previous_questions"]

        questions = Question.query.filter_by(category=category_id).filter(
            Question.id.notin_((previous_questions))).all()

        questions = [question.format() for question in questions]

        return jsonify({
            "question": random.choice(questions) if questions else None,
            "success": True
        })

    @app.errorhandler(400)
    def not_found(error):
        '''
        Error handler for the HTTP code 400 : Bad Request
        '''

        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        '''
        Error handler for the HTTP code 404 : Not Found
        '''

        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        '''
        Error handler for the HTTP code 422 : Unprocessable
        '''

        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def not_found(error):
        '''
        Error handler for the HTTP code 500
        '''

        return jsonify({
            "success": False,
            "error": 500,
            "message": "Something went wrong"
        }), 500

    return app
