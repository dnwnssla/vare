from flask import Flask, g, request, Response, make_response, session
from flask import render_template, redirect,session, flash
#from datetime import date, datetime, timedelta
from helloflask.init_db import init_database, db_session
from helloflask.models import Paitent,Doctor,Diagnosi,DiagDoc,MedicalHistory,Reservation,HosEvalu,DocEvalu
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.debug = True
app.secret_key = "2345xc12"


@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/', methods=['POST'])
def index():
    diag_f = request.form.get('diag_id')
    log = Diagnosi.query.filter(Diagnosi.diag_id==diag_f).first()
    pait = Paitent.query.filter(Paitent.pat_id == log.pat_id).first()
    print(log.diag_id + pait.pat_name)
    if log is not None:
     session['loginUser'] = { 'userid':log.diag_id, 'name': pait.pat_name }
    else:
        flash("잘못된 고유번호 입니다.")
    return render_template('home.html')


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