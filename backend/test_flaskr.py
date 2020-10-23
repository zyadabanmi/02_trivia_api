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
        self.database_path = "postgres://{}/{}".format('postgres:1234Qwer@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.new_question = {
            'question': 'test questiuon ?',
            'answer': 'test answer',
            'category': '1',
            'difficulty': '2'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['currentCategory'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
            
    def test_404_request_page_beyond_limit(self):
        res = self.client().get('/questions?page=40')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
        
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories']))
            
    def test_404_request_unknown_endpoint_for_categories(self):
        res = self.client().get('/categoriess')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
        
    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], )
            
    def test_404_delete_using_unexisting_id(self):
        res = self.client().delete('/questions/100000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
        
    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
            
    def test_400_missing_fildes(self):
        res = self.client().post('/questions', json={"answer":"rwe","difficulty":1,"category":1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'Bad request')
        
    def test_400_not_included_body(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'Bad request')
        
    def test_search_question(self):
        res = self.client().post('/questions/search', json={"searchTerm":"clay"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['current_category'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
            
    def test_400_no_search_term_used(self):
        res = self.client().post('/questions/search', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'Bad request')
        
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(len(data['questions']))
            
    def test_404_not_exisiting_id_provided(self):
        res = self.client().get('/categories/1111111/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
        
    def test_get_next_question(self):
        res = self.client().post('/quizzes', json={"previous_questions":[],"quiz_category":{"type":"Sports","id":"6"}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
            
    def test_400_no_body_provided(self):
        res = self.client().post('/questions/search', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'Bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()