import os
from flask import Flask, request, abort, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from random import choice
from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
      try:
        categories = {category.id:category.type for category in Category.query.all()} 
        
        return jsonify({
          'categories': categories,
    })
      except:
        abort(422)
      
  


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_paginated_questions():
      categories = {category.id:category.type for category in Category.query.all()}
      page = request.args.get('page', 1, type=int)
      start =  (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      questions = [question.format() for question in Question.query.order_by(Question.id).all()][start:end]
        
      if (len(questions) == 0):
           abort(404)
            
      return jsonify({
          'questions': questions,
          'total_questions': len(Question.query.all()),
          'categories': categories,
          'currentCategory': 1
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
      question = Question.query.filter(Question.id == question_id).one_or_none()
      
      if question is None:
           abort(404)
            
      question.delete()
      return jsonify({
        'success': True,
        'deleted': question_id
      })
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
      new_question = request.get_json()
      
      if(len(request.get_json()) != 4):
            abort(400)
            
      question = Question(new_question['question'], new_question['answer'], new_question['category'], new_question['difficulty'])
      question.insert()
      return jsonify({
        'success': True,
        'question': new_question
      })
      

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
      if(len(request.get_json()) == 0):
            abort(400)
      search_term = "%{}%".format(request.get_json()['searchTerm'])
      questions = [question.format() for question in Question.query.filter(Question.question.ilike(search_term)).all()]
      return jsonify({
        'questions':questions,
        'total_questions': len(questions),
        'current_category': 1
      })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_categories_by_id(category_id):
      questions = [question.format() for question in Question.query.filter(Question.category == category_id).all()]
      
      if (len(questions) == 0):
           abort(404)
          
      return jsonify({
        'questions': questions,
        'total_questions': len(questions),
        'current_category': category_id
      })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_next_question():
        # refactore for all catgeoris 
      if(len(request.get_json()) == 0):
            abort(400)
      previous_questions = request.get_json()['previous_questions']
      quiz_category = request.get_json()['quiz_category']
      if(quiz_category['type'] == 'click'):
            questions = [question.format() for question in Question.query.all()]
      else:
            questions = [question.format() for question in Question.query.filter(Question.category == quiz_category['id']).all()]
            
      remaining_questions = []
      
      for question in questions:
            if (question['id'] not in previous_questions):
                  remaining_questions.append(question)
                  
      return jsonify({
        'question': choice(remaining_questions) if len(remaining_questions) else ''
      })
      

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
        'error': 400,
        'message': 'Bad request'
      }), 400
      
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
        'error': 404,
        'message': 'resource not found'
      }), 404
      
  @app.errorhandler(422)
  def unprocessable_entity(error):
      return jsonify({
        'error': 422,
        'message': 'unprocessable entity'
      }), 422
  
  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
        'error': 500,
        'message': 'Internal server error'
      }), 500
  
  return app

    