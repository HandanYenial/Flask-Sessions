from flask import Flask,request,render_template,redirect,flash,session
from surveys import satisfaction_survey # as survey 
#as is to rename. Since writing satisfaction_survey is long, we write down survey. it could be anything.

from flask_debugtoolbar import DebugToolbarExtension

#RESPONSES_KEY = "responses"
responses=[]
#Storing answers in a list on the server has some problems. 
#The biggest one is that there’s only one list – if two people try to answer
#the survey at the same time, they’ll be stepping on each others’ toes!
#A better approach is to use the session to store response information, 


app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False #when we don't add this it shows a message as 
# "The Flask Debug Toolbar has intercepted a redirect to the above URL for debug viewing purposes..."
#everytime we have a redirect


debug = DebugToolbarExtension(app)


#When the user goes to the root route, render a page that shows the user the title of the survey, 
# the instructions, and a button to start the survey. 

@app.route('/')
def show_survey_title():
    return render_template("start-page.html", satisfaction_survey=satisfaction_survey)
    session["responses"] = []
    #To begin, modify your start page so that clicking on the button fires off a POST
    #request to a new route that will set session[“responses”] to an empty list.
# The button should serve as a link that directs the user to /questions/0 
# (the next step will define that route).
  
@app.route('/questions', methods=["POST"])
def show_question():
     return redirect("/questions/0")

#When the user arrives at one of these pages, it should show a form asking the 
# current question, and listing the choices as radio buttons.
# Answering the question should fire off a POST request to /answer with the 
# answer the user selected

@app.route("/answer", methods=["POST"])
def get_answer():
    choice=request.form['answer'] #get the response choice  
    responses=session["responses"]
    responses.append(choice)
    session["responses"] = responses
    #When it comes time to modify the session, watch out.
    #Normally, you can append to a list like this:fruits.append("cherry")
    #However, for a list stored in the session, you’ll need to rebind the name in the session, like so:
    #fruits = session['fruits']
    #fruits.append("cherry")
    #session['fruits'] = fruits
    
    len(responses) != 0 #if it doesn't have this then when clicked to start, it redirects to completion page.
    if (len(responses) == len(satisfaction_survey.questions)):
            # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")
    
#When the user submits an answer, you should append this answer to your 
# responses list,and then redirect them to the next question.
#The customer satisfaction survey only has 4 questions, so once the 
# user has submitted four responses, there is no new question to task.
# Once the user has answered all questions, rather than trying to send 
# them to /questions/5, redirect them to a simple “Thank You!” page.


#if the user has answered one survey question, but then tries to manually enter questions/4
#in the url bar redirect them to to /questions/1
@app.route("/questions/<int:qid>")
def the_question(qid):
    """Display current question."""

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != qid):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {qid}.")  #if the user does try to visit questions out of order, flash message.
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[qid]
    return render_template(
        "thank.html", question_num=qid, question=question)

@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("complete.html")

   
    
    
    