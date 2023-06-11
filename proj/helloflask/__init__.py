from flask import Flask, g, request, Response, make_response, session
from flask import render_template, redirect,session, flash
#from datetime import date, datetime, timedelta
from helloflask.init_db import init_database, db_session
from helloflask.models import Paitent,Doctor,Diagnosi,DiagDoc,MedicalHistory,Reservation,HosEvalu,DocEvalu
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.debug = True
app.secret_key = "2345xc12"


@app.route('/')
def index():    
    return render_template('login.html',title="login.html")

@app.route('/home')
def home():    
    return render_template('home.html',title="main")

@app.route('/hospital')
def hospital():    
    return render_template('hoste.html',title='hoste.html')

@app.route('/doctor')
def doctor():    
    return render_template('doce.html',title='doce.html')

@app.route('/reservation')
def reservation():    
    return render_template('reser.html',title='reser.html')

@app.route('/history')
def history():    
    return render_template('histo.html',title='histo.html')