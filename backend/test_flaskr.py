import os
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
            'category': 1
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # Test get all categories
    #------------------------------------------------------------#
    def test_get_all_categories(self):
        res = self.client().get("/api/v1/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]), 6) # check if the six (6) categories is returned

    # Test get all categories
    #------------------------------------------------------------#
    def test_get_paginated_questions(self):
        res = self.client().get("/api/v1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]), 10) # Check if 10 questions are returned

    # Test get 404 error when page is beyond available page
    #------------------------------------------------------------#
    def test_404_error_beyond_available_page(self):
        res = self.client().get("/api/v1/questions?page=25")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'Resource not found')

    # Test Delete question with specific id
    #------------------------------------------------------------#
    def test_delete_question(self):
        res = self.client().delete("/api/v1/questions/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        
    # Test Delete question with specific id
    #------------------------------------------------------------#
    def test_delete_question_error_404_unexisted_id(self):
        res = self.client().delete("/api/v1/questions/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'Resource not found')

    # Test create question
    #------------------------------------------------------------#
    def test_create_question(self):
        res = self.client().post("/api/v1/questions", data=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["message"], 'Bad Request')

    # Test create question bad payload
    #------------------------------------------------------------#
    def test_create_question_bad_request(self):
        res = self.client().post("/api/v1/questions", data=self.new_bad_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'Bad Request')

    
    



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()