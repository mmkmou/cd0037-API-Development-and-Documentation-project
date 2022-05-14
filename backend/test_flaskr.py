import os
from unicodedata import category
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgres://{}:{}@{}/{}'.format('postgres','Pa553R','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'What is the best learning platform ?',
            'answer': 'udacity',
            'difficulty': 1,
            'category': 2
        }

        self.new_bad_question = {
            'question': 'What is the best learning platform ?',
            'answer': 'udacity',
            'difficulty': 'Difficulty',
            'category': 2
        }
    
        self.quizzes = {
            "previous_questions": [22, 21],
            "quiz_category": {
                "id": 1,
                "type": "Science"
            }
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    
    # Test get all categories
    #------------------------------------------------------------#
    def test_get_all_categories(self):
        res = self.client().get("/api/v1/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    # Test get all questions
    #------------------------------------------------------------#
    def test_get_paginated_questions(self):
        res = self.client().get("/api/v1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertTrue(data["current_category"])

    # Test get 404 error when page is beyond available page
    #------------------------------------------------------------#
    def test_404_error_beyond_available_page(self):
        res = self.client().get("/api/v1/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'resource not found')
        
    # Test Delete question with specific id
    #------------------------------------------------------------#
    def test_delete_question(self):
        res = self.client().delete("/api/v1/questions/10")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 10)
        self.assertEqual(question, None)


    # Test Delete unexisted question
    #------------------------------------------------------------#
    def test_422_error_delete_unexisted_question(self):
        res = self.client().delete("/api/v1/questions/100000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'unprocessable')


    # Test create question
    #------------------------------------------------------------#
    def test_create_question(self):
        res = self.client().post("/api/v1/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # Test create question bad payload
    #------------------------------------------------------------#
    def test_400_error_create_question(self):
        res = self.client().post("/api/v1/questions", json=self.new_bad_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'bad request')
    

    # Test get question by category
    #------------------------------------------------------------#
    def test_get_question_by_category(self):
        res = self.client().get("/api/v1/categories/1/questions")
        data = json.loads(res.data)

        category = Category.query.filter(Category.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertEqual(data["current_category"], "Science")
        

    # Test get question from unexisted category
    #------------------------------------------------------------#
    def test_400_ERROR_get_question_by_unexisted_category(self):
        res = self.client().get("/api/v1/categories/10000/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'bad request')


    # Test search questions by terms
    #------------------------------------------------------------#
    def test_search_question_by_terms(self):
        res = self.client().post("/api/v1/questions", json={"searchTerm": "autobiography"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])

    # Quizzes
    #------------------------------------------------------------#
    def test_quizze(self):
        res = self.client().post("/api/v1/quizzes", json=self.quizzes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["question"]["id"],20)
        self.assertEqual(data["question"]["category"], 1)
    



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()