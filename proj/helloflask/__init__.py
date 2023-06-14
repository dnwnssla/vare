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
        session['loginUser'] = { 'userid':log.diag_id, 'name': pait.pat_name ,'pat_id': pait.pat_id}
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

@app.route('/hospital',methods=['GET'])
def hospital():
    item = EvaluteItem.query.filter(EvaluteItem.target == "병원").order_by(EvaluteItem.type).all()
    mlist=["매우만족", "만족", "보통", "불만족", "매우불만족"]

    return render_template('hoste.html',evallist=item, mlist=mlist)

@app.route('/hospital',methods=['POST'])
def hospital_post():
    eval_list = EvaluteItem.query.filter(EvaluteItem.target == "병원").order_by(EvaluteItem.type).all()
    userinfo= session.get('loginUser')
    pid=userinfo['pat_id']
    did =userinfo['userid']
   
    for item in eval_list:  
        item_value = request.form.get(str(item.evalu_id))      
        u = HosEvalu(pat_id = pid, diag_id = did,evalu_id =item.evalu_id, evalu_ans=item_value)
        db_session.add(u)
    db_session.commit()
    return render_template('home.html')
    
@app.route('/doctor', methods=['GET'])
def doctor():
    diag = DiagDoc.query.filter(DiagDoc.diag_id,DiagDoc.pat_id,DiagDoc.doc_id)
    doc = Doctor.query.filter(Doctor.doc_id==DiagDoc.doc_id).all()
    item = EvaluteItem.query.filter(EvaluteItem.target == "의사").order_by(EvaluteItem.type).all()
    mlist=["매우만족", "만족", "보통", "불만족", "매우불만족"]
#    print(item)   
    return render_template('doce.html',evallist=item, mlist=mlist, doclist= doc)    

@app.route('/doctor', methods=['POST'])
def doctor_post():
    doc = Doctor.query.filter(Doctor.doc_id==DiagDoc.doc_id).all()
    evalu_list = EvaluteItem.query.filter(EvaluteItem.target == "의사").order_by(EvaluteItem.type).all()
    userinfo = session.get('loginUser')
    pid=userinfo['pat_id']  
    did = userinfo['userid']
    for doc_list in doc:
        for item in evalu_list:
            item_value=request.form.get(str(item.evalu_id))
            du = DocEvalu(pat_id = pid, diag_id = did, doc_id = doc_list.doc_id, evalu_id = item.evalu_id, evalu_ans=item_value)
            db_session.add(du)
        db_session.commit()
    
    return render_template('home.html')   



@app.route('/reservation')
def reservation():
    return render_template('reser.html',title='reser.html')

@app.route('/history')
def history():    
    return render_template('histo.html',title='histo.html')