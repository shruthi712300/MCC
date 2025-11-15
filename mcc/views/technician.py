from flask import render_template, request, redirect, url_for

from .. import app, crud, util, models


@app.get("/tech/work")
def tech_dashboard():
    technician = util.current_user_info(request)
    print(technician)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    
    return  render_template ("tech_dashboard.html", technician=technician ,work = crud.get_work_by_tech_id(technician.technician_id))
    """return render_template("tech_dashboard.html", technician=technician , 
                           get_onsitetask_tech_count=crud.get_onsitetask_tech_count(username=technician.username),
                           get_instore_task_tech_count=crud.get_instore_task_tech_count(username=technician.username)
                           ,get_instore_task_tech_ready_count=crud.get_instore_task_tech_ready_count(username=technician.username))

"""
@app.get("/tech/onsite")
def tech_onsite():
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    return render_template(
        "tech_onsite.html",
        customers=crud.get_all_customer(),
        tasks=crud.get_onsitetasks_by_tech(username=technician.username), technicians=crud.get_all_technicians(),
        technician=technician
    )

@app.post("/tech/onsite")
def tech_onsite_add_task():
    technician = util.current_user_info(request)
    data = dict(request.form)
    
    if data.get("ftype"):
        return render_template(
            "tech_onsite.html",
            customers=crud.get_all_customer(),
            tasks=crud.get_onsitetasks_by_tech(username=technician.username,filter=data), technicians=crud.get_all_technicians(),
            technician=technician, 
        )

    try:
        crud.create_task(data)
    except Exception as e:
        return render_template(
            "tech_onsite.html",
            customers=crud.get_all_customer(),
            tasks=crud.get_onsitetasks_by_tech(username=technician.username), technicians=crud.get_all_technicians(),
            technician=technician,
            errors=str(e).split(",")
        )
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    return render_template(
        "tech_onsite.html",
        customers=crud.get_all_customer(),
        tasks=crud.get_onsitetasks_by_tech(username=technician.username), technicians=crud.get_all_technicians(),
        technician=technician
    )

@app.get("/tech/onsite/viewtask/<task_id>")
def tech_onsite_task_view(task_id):
    print((crud.get_resources_by_id(task_id)))
    data = models.Items.query.filter_by(task_id=task_id).all()
    return render_template(
        "tech_onsite_task_view.html",
        tasks=crud.get_onsitetask_by_id(task_id),
        resources=crud.get_resources_by_id(task_id), technicians=crud.get_all_technicians(),data=data,
    )


@app.post("/tech/onsite/viewtask/<task_id>")
def tech_onsite_task_update(task_id):
    data = dict(request.form)
    data["task_id"] = task_id
    message = ""
    task = crud.get_onsitetask_by_id(task_id)
    if task and (task.status == "Pending"):
        try:
            crud.update_onsitetasks(data)
            message = "Task Updated Successfully"
        except Exception as e:
            message = str(e).split(",")
    else:
        message="Already ready"
    
    return render_template(
        "tech_onsite_task_view.html",
        tasks=crud.get_onsitetask_by_id(task_id),
        resources=crud.get_resources_by_id(task_id),
        message=message,
    )

@app.get("/tech/onsite/<task_id>/update_status")
def tech_onsite_update_status(task_id):
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    resource = crud.get_resources_by_id(task_id=task_id)
    message=""
    if not resource:
        message="Update resource first"
    elif resource.received_charge < resource.service_charge:
        message="Service charge is not received"
    else:
        flag = crud.update_onsite_task_status(task_id)
        if flag:
            message="Status updated"
        else:
            message="Already ready"
    return render_template(
        "tech_onsite_task_view.html",
        tasks=crud.get_onsitetask_by_id(task_id),
        resources=crud.get_resources_by_id(task_id),
        message=message,
    )

@app.get("/tech/customer")
def tech_customer():
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    return render_template("tech_customer.html", customers=crud.get_all_customer())


@app.post("/tech/customers")
def tech_customers_filter():
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    data = dict(request.form)
    if data.get("ftype"):
        return render_template(
            "tech_customer.html",
            customers=crud.get_all_customer(filter=data)
            
        )
    return redirect(url_for("customers"))
@app.get("/tech/customers/work/onsite/<customer_id>")
def tech_customer_onsite_task_view(customer_id):
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    
    return render_template(
        "tech_onsite_work_view.html",
        tasks=crud.get_onsitetask_by_cust_id(customer_id)
    )

@app.get("/tech/customers/work/instore/<customer_id>")
def tech_customer_instore_task_view(customer_id):
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    
    return render_template(
        "tech_instore_work_view.html",tasks=crud.get_instoretask_by_cust_id(customer_id))

@app.get("/tech/instore")
def tech_instore():
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    return render_template("tech_instore.html",tasks=crud.get_instoretasks_by_tech(username=technician.username))

@app.post("/tech/instore")
def tech_instore_filter_task():
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    data = dict(request.form)
    if data.get("ftype"):
        return render_template(
            "tech_instore.html",tasks=crud.get_instoretasks_by_tech(username=technician.username,filter=data)
        )
    return redirect(url_for("tech_instore"))

@app.get("/tech/instore/add")
def tech_instore_add_task():
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    return render_template(
        "tech_instore_add_task.html", tasks=crud.get_instoretasks_by_tech(username=technician.username), 
        technicians=crud.get_all_technicians(),flag=False,technician=technician, 
    )

@app.post("/tech/instore/add")
def tech_instore_add_task_view():
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    data = dict(request.form)
    crud.create_instore_task(data)

    return render_template(
        "tech_instore_add_task.html",
        
        tasks=crud.get_instoretasks_by_tech(username=technician.username),technicians=crud.get_all_technicians(),technician=technician, 
        flag=False,
    )

@app.get("/tech/instore/task/<task_id>")
def tech_instore_task_view_by_id(task_id):
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    return render_template(
        "tech_instore_add_task.html",
        flag=True,
        tasks=crud.get_instoretask_by_id(task_id),
        technicians=crud.get_all_technicians(),technician=technician, 
    )

@app.post("/tech/instore/task/<task_id>")
def tech_instore_task_update(task_id):
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    data = dict(request.form)
    data["task_id"] = task_id
    crud.update_instoretasks(data)
    return render_template(
        "tech_instore_add_task.html",
        flag=True,
        tasks=crud.get_instoretask_by_id(task_id),
        technicians=crud.get_all_technicians()
    )



#####WORK#######
@app.get("/tech/work")
def tech_work():
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="technician") or not technician:
        return render_template("check.html")
    return render_template(
        "tech_work.html",technician=technician,work = crud.get_work_by_tech_id(technician.technician_id)
            
    )


@app.post("/tech/work")
def work_add_task():
    technician = util.current_user_info(request)
    if (not util.is_user_authenticated(request,type="technician") or not technician) :
        return render_template("check.html")
    data = dict(request.form)
    print(data)
    
    if data.get("ftype"):
        return render_template(
            "tech_work.html",technician=technician,work = crud.get_work_by_tech_id(technician.technician_id,filter=data)
            
        )
    try:
        crud.add_work(data,technician.technician_id)
    except Exception as e:
        return render_template(
            "tech_work.html",
        )
    
    return redirect(url_for("tech_work"))

@app.get("/tech/onsite/<task_id>/customerreview")
def tech_onsite_customer_review(task_id):
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    
    return render_template(
        "customer_review.html",
        tasks=crud.get_onsitetask_by_id(task_id),
        resources=crud.get_resources_by_id(task_id),task_id=task_id,
        message="",
    )

@app.post("/tech/onsite/<task_id>/customerreview")
def tech_onsite_customer_review_update(task_id):
    data = dict(request.form)
    print(data)

    try:
        crud.add_customer_review(data)
    except Exception as e:
        return render_template(
            "customer_review.html",
            tasks=crud.get_onsitetask_by_id(task_id),
            resources=crud.get_resources_by_id(task_id),
            message=str(e).split(",")
        )
    """
    data["task_id"] = task_id
    message = ""
    task = crud.get_onsitetask_by_id(task_id)
    if task and (task.status == "Pending"):
        try:
            crud.update_onsitetasks(data)
            message = "Task Updated Successfully"
        except Exception as e:
            message = str(e).split(",")
    else:
        message="Already ready"
    """
    return render_template(
        "customer_review.html",
        tasks=crud.get_onsitetask_by_id(task_id),
        resources=crud.get_resources_by_id(task_id),technicians=crud.get_all_technicians(),task_id=task_id,
    
    )