from email.policy import default
from logging import NullHandler
import string
from tokenize import Double
from .. import db, app
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
)
from sqlalchemy.orm import relationship


class Admin(db.Model):
    __tablename__ = "admins"
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    username = Column(String(20), primary_key=True)
    password = Column(String(20), nullable=False)
    phone_no = Column(String(20), nullable=False)


class Technician(db.Model):
    __tablename__ = "technician"
    technician_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    username = Column(String(20), primary_key=True)
    password = Column(String(20), nullable=False)
    phone_no = Column(String(20), nullable=False)
    status = Column(String(20),default="Active")


class OnsiteTask(db.Model):
    __tablename__ = "onsite_task"
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    t_name = Column(String(2),default="ON")
    date = Column(Date, nullable=False)
    creation_date = Column(Date)
    #customer_id = Column(Integer, ForeignKey("customer.customer_id"))
    customer_name = Column(String(30))
    phone_no = Column(BigInteger)
    address = Column(String(25))


    technician_id = Column(Integer, ForeignKey("technician.technician_id"))
    technician_id_2 = Column(Integer, ForeignKey("technician.technician_id"))
    service_type = Column(String(20), nullable=False)
    problem = Column(String(20), nullable=False)
    status = Column(String(20), default="Pending")
    technician = relationship("Technician", foreign_keys=[technician_id])
    technician2 = relationship("Technician", foreign_keys=[technician_id_2])
    #customer = relationship("Customer")


class Resources(db.Model):
    __tablename__ = "resources"
    task_id = Column(Integer, ForeignKey("onsite_task"), primary_key=True)
    material = Column(String(20), nullable=False)
    service_charge = Column(Integer, nullable=True)
    received_charge = Column(Integer, nullable=True)
    update_date = Column(Date)
    
    review = Column(String(70))


class Customer(db.Model):
    __tablename__ = "customer"
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False)
    phone_no = Column(String(10), nullable=False)
    address = Column(String(25))


class InstoreTask(db.Model):
    __tablename__ = "instore_task"
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    t_name = Column(String(2),default="IN")
    date = Column(Date, nullable=False)
    service_type = Column(String(20), nullable=False)
    status = Column(String(20))
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))

    product_id = Column(Integer, ForeignKey("product.product_id"))
    technician_id = Column(Integer, ForeignKey("technician"))
    problem = Column(String(20), nullable=False)

    est_days = Column(Integer)
    est_charge = Column(Integer)
    final_charge = Column(Integer)
    recived_charge = Column(Integer)
    discount = Column(Integer)
    remarks = Column(String(70))
    items_received = Column(String(70), nullable=False)
    serial_no = Column(String(70))
    bag = Column(String(3))
    charger = Column(String(3))
    power_cable = Column(String(3))
    delivery_date = Column(Date)
    open_date = Column(Date)
    close_date = Column(Date)
    delivered_by = Column(String(20))
    update_date = Column(Date)
    product_name_in = Column(String(40))
    product_company_in = Column(String(40)) 

    technician = relationship("Technician")
    customer = relationship("Customer")
    product = relationship("Products")


class Products(db.Model):
    __tablename__ = "product"
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(20), nullable=False)
    product_company = Column(String(20))

class Items(db.Model):
    __tablename__ = "items"
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    sl_no = Column(Integer)
    task_id = Column(Integer, ForeignKey("onsite_task.task_id"))
    item_name = Column(String(30), nullable=False)
    serial_no = Column(String(25))
    nos = Column(Integer)
    mat_status = Column(String(20))

class Partners(db.Model):
    __tablename__ = "partners"
    partner_id = Column(Integer, primary_key=True, autoincrement=True)
    partner_name = Column(String(20), nullable=False,primary_key=True)
    phone_no = Column(String(10), nullable=False)
    partner_address = Column(String(20))


class Chiplevel(db.Model):
    __tablename__ = "chiplevel"
    chiplevel_id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("instore_task.task_id"))
    status = Column(String(20))
    outward_date = Column(Date, nullable=False)
    inward_date = Column(Date, nullable=True)
    est_days = Column(Integer)
    est_charge = Column(Integer)
    partner_charge = Column(Integer)
    recived_charge = Column(Integer)
    remarks = Column(String(70))
    items_sent = Column(String(70))
    partner_id = Column(Integer, ForeignKey("partners.partner_id"))

    partners = relationship("Partners")
    instoretask = relationship("InstoreTask")

class Warranty(db.Model):
    __tablename__ = "warranty"
    warranty_id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("instore_task.task_id"))

    status = Column(String(20))
    outward_date = Column(Date, nullable=False)
    inward_date = Column(Date)
    est_days = Column(Integer)
   
    work = Column(String(20))
    wtype = Column(String(20))
    remarks = Column(String(70))
    items_sent = Column(String(70))
    partner_id = Column(Integer, ForeignKey("partners.partner_id"))

    partners = relationship("Partners")
    instoretask = relationship("InstoreTask")

class Quotation(db.Model):
    __tablename__ = "quotation"
    quotation_no = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))
    customer_ph = Column(Integer)
    customer = relationship("Customer")
    
class OnsiteItems(db.Model):
    __tablename__="onsite_items"
    task_id = Column(Integer, ForeignKey("onsite_task"), primary_key=True)
    sn_no = Column(Integer)
    item_name = Column(String(20))
    item_serial = Column(String(20))

class Work(db.Model):
    __tablename__ = "work"
    work_id = Column(Integer, primary_key=True, autoincrement=True)
    t_name = Column(String(2),default="ON")
    service_date = Column(Date, nullable=False)
    creation_date = Column(Date)
    customer_name = Column(String(30))
    service_type = Column(String(20), nullable=False)
    problem = Column(String(20), nullable=False)
    status = Column(String(20))
    servicecharges = Column(Integer)
    receivedamount = Column(Integer)
    start_time = Column(String(20))
    end_time = Column(String(20))
    technician_id = Column(Integer, ForeignKey("technician"))

    technician = relationship("Technician")

class Customer_review(db.Model):
    __tablename__ = "customer_review"
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("onsite_task.task_id"))
    signature = Column(String(max))
    ratings  = Column(String(20))

    onsitetask = relationship("OnsiteTask")


class InstoreNew(db.Model):
    __tablename__ = "instore_new"
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    service_date = Column(Date)
    creation_date = Column(Date)
    status = Column(String(20))
    cname = Column(String(30))
    cphoneno = Column(String(20))
    service_type = Column(String(20))
    engineer_assign = Column(String(20))
    est_days = Column(Integer)
    est_charges = Column(Integer)
    product_type = Column(String(40))
    product_model = Column(String(40))
    problem = Column(String(40))
    serial_no = Column(String(40))
    power_cable = Column(String(40))
    bag = Column(String(40))
    charger = Column(String(40))
    product_status = Column(String(40))
    hard_disk_condition = Column(String(40))
    battery_condition = Column(String(40))
    display = Column(String(40))
    remarks = Column(String(100))
    other_accessories = Column(String(40))
    service_charge = Column(Integer)
    received_charge = Column(Integer)
    discount = Column(Integer)
    payment_status = Column(String(20))


class OnsiteNew(db.Model):
    __tablename__ = "onsite_new"
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    creation_date = Column(Date)
    urgency = Column(String(20))
    status = Column(String(40))
    on_service_date = Column(Date)
    cname = Column(String(30))
    cphoneno = Column(String(20))
    caddress = Column(String(20))
    service_type = Column(String(20))
    engineer_assign = Column(String(20))
    problem = Column(String(40))
    remarks = Column(String(100))
    service_charge = Column(Integer)
    received_charge = Column(Integer)
    discount = Column(Integer)
    payment_status = Column(String(20))

    
with app.app_context():
    db.create_all()
