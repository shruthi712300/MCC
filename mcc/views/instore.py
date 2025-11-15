from flask import render_template, request, redirect, url_for, make_response,json,Response, jsonify, send_file
import pymysql
from .. import app, crud, util, models, pdf,db
from sqlalchemy import or_, case
from fpdf import FPDF
import pytz
from  .. import msgtest
from datetime import datetime
# from ..msgtest import send_whatsapp_message
from .whatsapp_msg import send_whatsapp_msg
import requests

@app.route('/tally/whatsapp/msg', methods=['POST'])
def receive_and_forward():
    try:
        json_data = request.json  # Get incoming JSON
        destination_url = 'http://localhost:3000/send-message'  # Replace with actual msg.com URL

        # Forward data to msg.com
        response = requests.post(destination_url, json=json_data, headers={'Content-Type': 'application/json'})

        return jsonify({'message': 'Data forwarded successfully', 'response': response.json()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.get('/admin/instorenew')
def instorenew():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    
    instorenew = get_instorenew()

    
    
    return render_template('instorenew.html', instorenew=instorenew)

@app.post("/admin/instorenew")
def instorenew_filter():
    data = dict(request.form)
    names = crud.get_all_customer_phone()
    
    name_lit =[]
    for i in names:
        name_lit.append(i[0])
    if data.get("ftype"):
        print(data)
        return render_template(
            "instorenew.html",
            instorenew=crud.get_all_instoretasksnew(filter=data),
            technicians=crud.get_all_technicians(),phone=(name_lit)
            
        )
    return redirect(url_for("instorenew"))

def add_instorenew(data: dict):
    instask = models.InstoreNew(creation_date=datetime.now(pytz.timezone('Asia/Kolkata')),**data)
    #send_whatsapp_message(instask)
    db.session.add(instask)
    db.session.commit()
    db.session.flush()

def get_instorenew():
    instorenew = models.InstoreNew.query.order_by(models.InstoreNew.task_id.desc()).all()
    return instorenew

def get_instorenew_by_id(task_id):
    instorenew = models.InstoreNew.query.filter_by(task_id=task_id).first()
    return instorenew


@app.route('/admin/instorenew/add', methods=['GET', 'POST'])
def instorenew_add():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    

    if request.method == 'POST':
        data = dict(request.form)
        
        add_instorenew(data)
        # msgtest.send_whatsapp_message(data)
        print(data)


    return render_template('instorenew_add.html', tasks = {""},technicians=crud.get_all_technicians())


@app.get("/admin/instorenew/task/<task_id>")
def instorenew_task_view_by_id(task_id):
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    return render_template(
        "instorenew_add.html",
        flag=True,
        tasks=get_instorenew_by_id(task_id),technicians=crud.get_all_technicians()
    )


@app.post("/admin/instorenew/task/<task_id>")
def instorenew_task_update_by_id(task_id):
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    data = dict(request.form)
    task = get_instorenew_by_id(task_id)
    for key, value in data.items():
        setattr(task, key, value)
    db.session.commit()
    return render_template(
        "instorenew_add.html",
        flag=True,
        tasks=get_instorenew_by_id(task_id),technicians=crud.get_all_technicians()
    )




###############################################################################################################################################
@app.get('/admin/onsitenew')
def onsitenew():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    
    onsitenew = get_onsitenew()
   
    return render_template('onsitenew.html', onsitenew=onsitenew)

@app.post("/admin/onsitenew")
def onsitenew_filter():
    data = dict(request.form)
    names = crud.get_all_customer_phone()
    
    name_lit =[]
    for i in names:
        name_lit.append(i[0])
    if data.get("ftype"):
        print("hello", data)
        return render_template(
            "onsitenew.html",
            onsitenew=crud.get_all_onsitetasksnew(filter=data),
            technicians=crud.get_all_technicians(),phone=(name_lit)
            
        )
    return redirect(url_for("onsitenew"))
def add_onsitenew(data: dict):
    onsite = models.OnsiteNew(**data)
    try:
        send_whatsapp_msg(data)
    except Exception as e:
        print(e)
    db.session.add(onsite)
    db.session.commit()
    db.session.flush()

def get_onsitenew():
    onsitenew = models.OnsiteNew.query.order_by(models.OnsiteNew.task_id.desc()).all()
    return onsitenew


@app.route('/admin/onsitenew/add', methods=['GET', 'POST'])
def onsitenew_add():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    
    creation_date = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d')


    if request.method == 'POST':
        data = dict(request.form)
        
        add_onsitenew(data)
        # msgtest.send_whatsapp_message(data)
        print(data)


    return render_template('onsitenew_add.html',technicians=crud.get_all_technicians(),tasks={'creation_date': creation_date})


@app.get("/admin/onsitenew/task/<task_id>")
def onsitenew_task_view_by_id(task_id):
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    return render_template(
        "onsitenew_add.html",
        flag=True,
        tasks=get_onsitenew_by_id(task_id),technicians=crud.get_all_technicians()
    )

def get_onsitenew_by_id(task_id):
    onsitenew = models.OnsiteNew.query.filter_by(task_id=task_id).first()
    return onsitenew


@app.post("/admin/onsitenew/task/<task_id>")
def onsitenew_task_update_by_id(task_id):
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    
    data = dict(request.form)
    task = get_onsitenew_by_id(task_id)

    previos_status = task.status
    new_status = data.get('status')
    if previos_status != new_status:
        send_whatsapp_msg(data)

    for key, value in data.items():
        setattr(task, key, value)
    db.session.commit()
    return render_template(
        "onsitenew_add.html",
        flag=True,
        tasks=get_onsitenew_by_id(task_id),technicians=crud.get_all_technicians()
    )





#ECH ONSITE3333333333333333333333333333333333333333333333333333333333333333333333333333

@app.get("/tech/onsitenew")
def tech_onsitenew():
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    return render_template(
        "tech_onsitenew.html",
        tasks=get_onsitenew_by_engineer(username=technician.username), technicians=crud.get_all_technicians(),
        technician=technician
    )


def get_onsitenew_by_engineer(username):
    print(username)
    #fetch boh onsite engineer assigned and unassigned
    onsitenew = models.OnsiteNew.query.filter(
        or_(
            models.OnsiteNew.engineer_assign == username,
            models.OnsiteNew.engineer_assign == ''
        )
    ).order_by(
        case(
            (models.OnsiteNew.status == 'open', 1),
            else_=0
        ).desc()
    ).all()
    print(onsitenew)
    return onsitenew

@app.route('/tech/onsitenew/add', methods=['GET', 'POST'])
def tech_onsitenew_add():
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    
    creation_date = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d')


    if request.method == 'POST':
        data = dict(request.form)
        
        add_onsitenew(data)
        # msgtest.send_whatsapp_message(data)
        print(data)


    return render_template('tech_onsitenew_add.html',technicians=technician,tasks={'creation_date': creation_date})

@app.get("/tech/onsitenew/task/<task_id>")
def tech_onsitenew_task_view_by_id(task_id):
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    return render_template(
        "tech_onsitenew_add.html",
        flag=True,
        tasks=get_onsitenew_by_id(task_id),technicians=technician
    )


@app.post("/tech/onsitenew/task/<task_id>")
def tech_onsitenew_task_update_by_id(task_id):
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    
    data = dict(request.form)
    task = get_onsitenew_by_id(task_id)
    for key, value in data.items():
        setattr(task, key, value)
    db.session.commit()
    return render_template(
        "tech_onsitenew_add.html",
        flag=True,
        tasks=get_onsitenew_by_id(task_id),technicians=crud.get_all_technicians()
    )

@app.route('/download/instorenew/report/pdf/<task_id>')
def instorenew_download_report(task_id):
    
    try:
        task = get_instorenew_by_id(task_id)
        
        pdf = FPDF(orientation = 'l', unit = 'mm', format = 'A5')
        pdf.add_page()
         
        page_width = 180

        pdf.set_font('Times','B',30) 
        pdf.cell(page_width, 0.0, '', align='C')
        pdf.ln(0)

        pdf.set_font('Times','B',20) 
        pdf.cell(page_width, 5, 'COM CARE SERVICES', align='C')
        pdf.ln(5)

        pdf.set_font('Times','',16) 
        pdf.cell(page_width, 10, 'SERVICE REPORT',  align='C')
        pdf.ln(20)
        
        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'Task ID: '+str(task.task_id), ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(82)
        pdf.cell(page_width, 0.0, 'Date: '+str(task.service_date),ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'Status: '+str(task.status),ln=3)
        pdf.ln(10)

        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'Customer Name: '+(str(task.cname)).capitalize(), align='L',ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(135)
        pdf.cell(page_width, 0.0,'Phone no:'+str(task.cphoneno),ln=3)
        pdf.ln(10)
    

        # pdf.set_font('Times', '', 15)
        # pdf.cell(page_width, 0.0, 'Est Days: '+str(task.est_days), align='L',ln=3)
        # pdf.ln(0)

        pdf.set_font('Times', '', 15)
        # pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'Product Types: '+str(task.product_type), align='L',ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'Product Model: '+str(task.product_model), align='L',ln=3)
        pdf.ln(10)

        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'Problem: '+str(task.problem).capitalize(), ln=3)
        pdf.ln(10)
        
        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'Power Cable: '+str(task.power_cable).capitalize(), align='L', ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(82)
        pdf.cell(page_width, 0.0, 'Charger: '+str(task.charger).capitalize(), ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'Bag: '+str(task.bag).capitalize(), align='L', ln=3)
        pdf.ln(10)

        # pdf.set_font('Times', '', 15)
        # pdf.cell(page_width, 0.0, 'Product Details: '+str(task.product.product_company),align='L', ln=3)
        # pdf.ln(0)


        pdf.set_font('Times', '', 15)
        
        pdf.cell(page_width, 0.0, 'Payment Status: '+str(task.payment_status), ln=3)
        pdf.ln(10)


        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'Service Charges: '+str(task.service_charge), align='L', ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'Advance/Recived Amt: '+str(task.received_charge), ln=3)
        pdf.ln(10)

        #if task.status=="Delivered":
         #   pdf.set_font('Times','',15) 
          #  pdf.cell(page_width, 0.0, 'Deliverd on:'+str(task.delivery_date), align='L',ln=3)

        pdf.ln(15)
        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'For Com Care ', align='L', ln=3)
        
        

        pdf.set_font('Times','',15) 
        pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'Customer Sign')



        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'inline;filename=employee_report.pdf'})
    except Exception as e:
        print(e)
