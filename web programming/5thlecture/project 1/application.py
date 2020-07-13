import os, json
import requests
import flask_whooshalchemy as wa

from sqlalchemy.exc import IntegrityError, DataError

from flask import Flask, render_template, request, jsonify,redirect, url_for, logging, session,g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_session import Session
from flask_sqlalchemy  import SQLAlchemy


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["WHOOSH_BASE"]='whoosh'

Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route('/')
def register():
    return render_template("register.html")

######################################################## sign up ###############################################

@app.route("/signup", methods=['GET','POST'])
def signup():
    register= db.execute("SELECT * FROM register").fetchall()
    
    return render_template("signup.html")

@app.route("/success",methods=['GET','POST'])
def success():
    uname= request.form.get("uname")
    psw = request.form.get("psw")

    try:
        db.execute("INSERT INTO register ( username, password) VALUES (:username, :password) ",
             {"username":uname, "password": psw})
        db.commit()
        return render_template("success.html")

    except IntegrityError as e:
        return render_template("error.html")

##############################################################################################################
########################################################logging in#############################################

@app.route("/login", methods=['GET','POST'])
def login():
    return render_template("login.html")

@app.route('/validate', methods=['POST'])
def validate():
    uname= request.form.get("uname")
    psw = request.form.get("psw")
    
    usernamedata= db.execute("SELECT username FROM register WHERE username=:username",{"username":uname}).fetchone()
    passworddata= db.execute("SELECT password FROM register WHERE username=:username",{"username":uname}).fetchone()
    if usernamedata is None and psw!=passworddata:
        return render_template("error.html", message="incorrect username or password")
    else:
        session["logged_in"] = True
        session["user_name"] = uname
        return redirect(url_for('lsuccess'))
       

@app.route("/lsuccess",methods=['GET','POST'])
def lsuccess():
     return render_template("lsuccess.html")
     
     
######################################################## LOGOUT ####################################################################

@app.route("/logout",methods=['GET','POST'])
def logout():
    session["logged_in"] = False
    session["user_name"] = None
    return render_template("register.html")


##################################################### MAIN PAGE ################################################################

@app.route("/page",methods=['GET','POST'])
def page():
    book=db.execute("SELECT * FROM books").fetchall()
    return render_template("page.html",book=book)


#########################################################  search #######################################################################
@app.route("/search",methods=['GET','POST'])
def search():
    search = f"%{request.form.get('term')}%"
    books = db.execute("SELECT * FROM books WHERE title LIKE :search OR author LIKE :search OR isbn LIKE :search",{'search':search}).fetchall()
    return render_template("books.html", books=books)
      

@app.route("/books",methods=['GET','POST'])
def books():
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("books.html", books=books)


@app.route("/books/<isbn>", methods=['GET','POST'])  #bookpage
def book(isbn):
    
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    
    if book is None:
        return render_template("error.html", message="No such book.")
    
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "4RbGuzka0IUcJWWk1mivqg", "isbns": isbn}).json()

    data= res
    
    avg_rating = float(data['books'][0]['average_rating'])
    work_ratings_count = float(data['books'][0]['work_ratings_count'])

    return render_template("book.html", book=book,avg_rating=avg_rating,work_ratings_count=work_ratings_count)

######################################################## review submission #########################################################

@app.route('/submit/<isbn>', methods=['POST'])
def bookreview(isbn):
    username=request.form.get("uname")
    review_rating = request.form.get("rating")
    review_text = request.form.get("review")
    isbn = isbn
    review = db.execute("SELECT * FROM book_review WHERE isbn = :isbn", {"isbn": isbn}).fetchall()


    try:
        usr= db.execute("SELECT username FROM book_review WHERE isbn=:isbn AND username=:username",{"isbn":isbn,"username":username}).fetchone()

        if usr is None:
            db.execute("INSERT INTO book_review ( username,review_rating , review_text, isbn ) VALUES (:username,:review_rating, :review_text, :isbn) ",
                    {"username":username,"review_rating":review_rating, "review_text": review_text,"isbn":isbn})
            db.commit()
            return render_template("bookreview.html",review=review,review_rating=review_rating,review_text=review_text,username=username)
    
        else:
            return render_template("error.html",message="The user has already reviewed this book")
            
    except IntegrityError as e:
        return render_template("error.html",message="the review has already been given by this username or specify the username correctly")
    
########################################################### showing review of this site ############################################

@app.route('/review/<string:isbn>', methods=['GET','POST'])
def showreviews(isbn):

    review = db.execute("SELECT * FROM book_review WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
    if review:
        return render_template("showreviews.html", review=review)

    else:
        return render_template("error.html", message="No reviews yet.")

#########################################################/api#################################################################

@app.route('/api/<string:isbn>', methods = ['GET'])
def isbn(isbn):
    #import api from Goodreads (stats)

    book_data = db.execute("SELECT * FROM books WHERE isbn=:isbn",{'isbn':isbn}).fetchone()
    title = book_data['title']
    author = book_data['author']
    year = book_data['year'] 

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "4RbGuzka0IUcJWWk1mivqg", "isbns":isbn }).json()
    if not res:
        return render_template("error.html",message="404, NOT FOUND")
    reviews_count = float(res['books'][0]['reviews_count'])
    avg_score = float(res['books'][0]['average_rating'])
    dic = {"title": title, "author":author, "year": year,"isbn":isbn,"reviews_count":reviews_count,"avg_score":avg_score}
    print(dic)
    return jsonify(dic)
    