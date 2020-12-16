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
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
  def __get_categories():
        categories = db.session.query(Category.id, Category.type).all()
        categories = {id: type.lower() for id, type in categories}
        return categories


@app.route("/categories")
def get_categories():
        categories = __get_categories()
        if len(categories) == 0:
            abort(404)
        else:
            return jsonify({"success": True, "categories": categories})




  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
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
    }) @app.route("/questions")

    def get_questions():
        page = request.args.get("page", 1, type=int)
        data = (
            db.session.query(Question)
            .order_by(Question.id)
            .slice((page - 1) * 10, page * 10)
            .all()
        )
        categories = __get_categories()
        questions = [q.format() for q in data]
        total_questions = db.session.query(Question).count()
        if total_questions == 0:
            abort(404)
        else:
            current_category = questions[0]["category"]  # NOTE: ok?
            return jsonify(
                {
                    "success": True,
                    "questions": questions,
                    "total_questions": total_questions,
                    "current_category": current_category,
                    "categories": categories,
                }
            )

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
   @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_questions(question_id):
      
        error = False
        question = Question.query.filter(
            Question.id == question_id
        ).one_or_none()
        if  question is None:
             abort(404)
        try:
             question.delete()
             question = question.format()
        except Exception:
             error = True
             db.session.rollback()
        finally:
             db.session.close()
        if not error:
             question["success"] = True
             return jsonify(question)
        else:
            abort(422


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

   @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_questions(question_id):
        error = False
        question = Question.query.filter(
            Question.id == question_id
        ).one_or_none()
        if question is None:
            abort(404)
        try:
            question.delete()
            question = question.format()
        except Exception:
            error = True
            db.session.rollback()
        finally:
            db.session.close()
        if not error:
            question["success"] = True
            return jsonify(question)
        else:
            abort(422

      

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''


    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        data = request.json
        search_term = data["search_term"]
        data = (
            db.session.query(Question)
            .filter(Question.question.ilike(f"%{search_term}%"))
            .all()
        )
        questions = [q.format() for q in data]
        total_questions = len(questions)
        if total_questions > 0:
            current_category = questions[0]["category"]  # NOTE: ok?
            response = {
                "questions": questions,
                "total_questions": total_questions,
                "current_category": current_category,
            }
            return jsonify(response)
        else:
            # TODO: render a page which says "No results are found".
            abort(404)
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
     def __get_questions_by_category(category_id):
        if category_id == 0:
            data = db.session.query(Question).all()
        else:
            data = (
                db.session.query(Question)
                .filter(Question.category == category_id)
                .all()

            )
        return [q.format() for q in data]


    @app.route("/categories/<int:category>/questions")
    def get_questions_by_category(category):

        questions = __get_questions_by_category(category)
        total_questions = len(questions)

        if total_questions > 0:
            response = {

                "questions": questions,
                "total_questions": total_questions,
                "current_category": category

            }

            return jsonify(response)
        else:

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
   @app.route("/quizzes", methods=["POST"])
    def get_quizzes():
       data = request.json
       previous_questions = set(data["previous_questions"])
       quiz_category_d = data.get("quiz_category", {})
       quiz_category = int(quiz_category_d["id"])
       questions = __get_questions_by_category(quiz_category)
       questions = [q for q in questions if q["question"] not in previous_questions]
        if len(questions) > 0:
            question = random.sample(questions, 1)[0]
            response = {"success": True, "question": question}
            return jsonify(response)
        else:
            abort(404)

      

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
    def not_found(error):
        return (jsonify({"success": False, "error": 404, "message": "Not found"}),404,)

@app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),422,)
    return app


    
