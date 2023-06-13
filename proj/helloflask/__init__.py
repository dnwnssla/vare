from flask import Flask, g, request, Response, make_response, session
from flask import render_template, redirect,session, flash
#from datetime import date, datetime, timedelta
from helloflask.init_db import init_database, db_session
from helloflask.models import Paitent,Doctor,Diagnosi,DiagDoc,Reservation,HosEvalu,DocEvalu,EvaluteItem
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.debug = True
app.secret_key = "2345xc12"


@app.route('/', methods=['GET'])
def login_get():
    return render_template('login.html')

@app.route('/', methods=['POST'])
def login_post():
    diag_f = request.form.get('id')
    
    log = Diagnosi.query.filter(Diagnosi.diag_id==diag_f).first()
    if log is not None:
        pait = Paitent.query.filter(Paitent.pat_id == log.pat_id).first()
        session['loginUser'] = { 'userid':log.diag_id, 'name': pait.pat_name }
        if session.get('next'): 
            next = session.get('next')
            del session['next']
            return redirect(next)
        return redirect('/home')
    else:
        flash("잘못된 고유번호 입니다.")
        return render_template('login.html')


@app.route('/logout')
def logout():
    if session.get('loginUser'):
        del session['loginUser']
    return redirect('/')


@app.route('/home')
def home():    
    return render_template('home.html',title="main")

@app.route('/hospital')
def hospital():
    item = EvaluteItem.query.filter(EvaluteItem.target == "병원").order_by(EvaluteItem.type).all()
    mlist=["매우만족", "만족", "보통", "불만족", "매우불만족"]
#    print(item)   
    return render_template('hoste.html',evallist=item, mlist=mlist)

@app.route('/doctor')
def doctor():
    diag = DiagDoc.query.filter(DiagDoc.diag_id,DiagDoc.pat_id,DiagDoc.doc_id).all()
    doc = Doctor.query.filter(Doctor.doc_id,Doctor.doc_name,Doctor.doc_major).all()
    item = EvaluteItem.query.filter(EvaluteItem.target == "의사").order_by(EvaluteItem.type).all()
    mlist=["매우만족", "만족", "보통", "불만족", "매우불만족"]
#    print(item)   
    return render_template('doce.html',evallist=item, mlist=mlist)    

@app.route('/reservation')
def reservation():
    return render_template('reser.html',title='reser.html')

@app.route('/history')
def history():    
    return render_template('histo.html',title='histo.html')