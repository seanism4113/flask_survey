from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

survey_responses = "responses"
satisfaction_survey = surveys.satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret-survey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def main_page():
    """ Select Survey """

    return render_template('main.html', survey = satisfaction_survey)

@app.route('/start_survey', methods=["POST"])
def start_survey():
    """ Start new survey and clear session of responses"""

    session[survey_responses] = []

    return redirect("/questions/0")

@app.route('/answers', methods=["POST"])
def handle_answers():
    """ Save answers to questions and go to next question """

    selection = request.form['answer']

    responses = session[survey_responses]
    responses.append(selection)
    session[survey_responses] = responses

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/complete')
    
    else:
        return redirect (f"/questions/{len(responses)}")


@app.route('/questions/<int:question_id>')
def display_questions(question_id):
    """ Show the question """

    responses = session.get(survey_responses)

    if (responses is None):
        return redirect('/')
    
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/complete')

    if (len(responses) != question_id):
        flash(f"Invalid questions ID: {question_id}")
        return redirect (f'/questions/{len(responses)}')

    question = satisfaction_survey.questions[question_id]

    return render_template('questions.html', question_id = question_id, question = question)

@app.route('/complete')
def survey_complete():
    return render_template('complete.html')