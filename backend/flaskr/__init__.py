from cmath import e
from operator import methodcaller
import os
from time import sleep
from unicodedata import category, name
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions
# Format the categories as dictionary
def format_categories(selection):
    categories = {}
    for category in selection:
        category = category.format()
        categories[str(category['id'])] = str(category['type'])

    return categories

#Handle question to get next_question
def handle_current_question(previous, selection):
    
    current_question = None
    for question in selection:
        if question.format()["id"] not in previous:
            current_question = question
            break

    return current_question

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    base_url = "/api/v1"

    
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE')
        return response

    # Get all categories
    #------------------------------------------------------------#
    @app.route(base_url + '/categories')
    def get_categories():
        selection = Category.query.order_by(Category.id).all()
        
        
        return jsonify({
            'success': True,
            'categories': format_categories(selection)
        })
    
    
    # Create an endpoint to handle GET requests for questions,
    #------------------------------------------------------------#
    @app.route(base_url + '/questions')
    def get_questions():
        questions = Question.query.order_by(Question.id).all()

        current_questions = paginate_questions(request, questions)

        categories =  format_categories(Category.query.all())
        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions":  len(questions),
                "categories": categories,
                "current_category": categories["1"]
            }
        )


    # Create an endpoint to DELETE question using a question ID.
    #------------------------------------------------------------#
    @app.route(base_url + "/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)
            
            question.delete()
            return jsonify(
                {
                    "success": True,
                    "deleted": question_id
                }
            )
        except Exception:
            abort(422)
    
    
    # Create / search a question,
    #------------------------------------------------------------#
    @app.route(base_url + '/questions', methods=["POST"])
    def create_search_question():
        body = request.get_json()
        search_term = body.get("searchTerm", None)
        if search_term == None:
            # create a new questions.
            try:
                question = Question(body.get("question", None), 
                                    body.get("answer", None),
                                    body.get("category", None),
                                    body.get("difficulty", None)
                                    
                                )
                question.insert()

                return jsonify(
                    {
                        "success": True
                    }
                )
                
            except Exception:
                abort(400)
        else:
            try:
                search = "%{}%".format(search_term)
                search_result = Question.query.filter(
                    Question.question.ilike(search)).all()
                questions = [question.format() for question in search_result]
                
                if len(questions) == 0:
                    abort(404)

                categories =  format_categories(Category.query.all())

                return jsonify(
                    {
                        "success": True,
                        "questions": questions,
                        "total_questions":  len(questions),
                        "current_category": categories["1"]
                    }
                )
            except Exception:
                abort(400)


    # Get questions based on category.
    #------------------------------------------------------------#
    @app.route(base_url + '/categories/<int:category_id>/questions')
    def get_questions_categories(category_id):
        try:
            questions = Question.query.filter(Question.category == category_id).all()
            print(len(questions))
            if len(questions) == 0:
                print("inside if ")
                abort(404)

            
            current_questions = paginate_questions(request, questions)

            categories =  format_categories(Category.query.all())
            

            
            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions":  len(questions),
                    "current_category": categories[str(category_id)]
                }
            )

        except Exception:
            abort(400)

    
    # Create a POST endpoint to get questions to play the quiz.
    #------------------------------------------------------------#
    @app.route(base_url + '/quizzes', methods=["POST"])
    def play_quiz():
        body = request.get_json()
        quiz_category = body.get("quiz_category")["id"]
        previous_questions =  body.get("previous_questions")
        if body.get("quiz_category")["id"] == 0:
            questions = Question.query.filter().order_by(func.random()).all()
        else:
            questions = Question.query.filter(Question.category == quiz_category).order_by(func.random()).all()

        
        current_question = handle_current_question(previous_questions, questions)


        if current_question != None:
            return jsonify(
                {
                    "success": True,
                    "question": current_question.format()
                }
            )
        else:
            return jsonify({})     

    # Handle 404 - 422 - 400 - 405 error.
    #------------------------------------------------------------#
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    return app

