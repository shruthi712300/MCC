from jose import jwt, JWTError
from flask import request, url_for, Request
from datetime import datetime, timedelta
from typing import Union

from . import crud, schemas, constants


def is_valid_password(username, password, role):
    if crud.get_password(username, role) == password:
        return True
    else:
        return False


def is_username_available(username: str, role: str) -> bool:
    if role == "admin":
        user = crud.get_admin(username)
    else:
        user = crud.get_technician(username)
    if user:
        return True
    return False


def is_partner_available(partner_name: str) -> bool:
    user = crud.get_partner(partner_name)
    if  user:
        return True
    return False


def is_customer_available(phone_no: str) -> bool:
    user = crud.get_customer_by_phone(phone_no)
    if user:
        return True
    return False


def is_task_rsources_available(task_id: int) -> bool:
    task = crud.get_resources_by_id(task_id)
    if task == None:
        return False
    else:
        return True


def is_product_available(product_name: str) -> bool:
    product = crud.get_product(product_name)
    if product:
        return True
    return False


def is_instore_task_available(task_id: int) -> bool:
    task = crud.get_instoretask_by_id(task_id)
    if task == None:
        return False
    else:
        return True
    
def is_on_work_available(work_id: int) -> bool:
    work = crud.get_work_by_id(work_id)
    if work == None:
        return False
    else:
        return True

def is_chiplevel_task_available(task_id: int) -> bool:
    task = crud.get_chiplevel_by_id(task_id)
    if task == None:
        return False
    else:
        return True

def is_warranty_task_available(task_id: int) -> bool:
    task = crud.get_warranty_by_id(task_id)
    if task == None:
        return False
    else:
        return True

def is_quotation_available(username: str, role: str) -> bool:
    if role == "admin":
        user = crud.get_admin(username)
    else:
        user = crud.get_technician(username)
    if user:
        return True
    return False


def is_phone_valid(phone_no: str) -> bool:
    if len(phone_no) == 10 and phone_no.isnumeric():
        return True
    return False

def is_service_charge_valid(service_charge: str) -> bool:
    if  service_charge.isnumeric():
        return True
    return False

def is_received_charge_valid(received_charge: str) -> bool:
    if  received_charge.isnumeric():
        return True
    return False
    

def create_access_token(
    data: schemas.TokenData, expires_delta: Union[timedelta, None] = None
):
    to_encode = dict(data).copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=constants.ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, constants.SECRET_KEY, algorithm=constants.ALGORITHM
    )
    return encoded_jwt


def get_current_user_login(token: str) -> Union[schemas.TokenData, None]:
    try:
        payload = jwt.decode(
            token, constants.SECRET_KEY, algorithms=[constants.ALGORITHM]
        )
        username: str = payload.get("username")
        id: str = payload.get("id")
        user_type: str = payload.get("user_type")
        if not username or not id or not user_type:
            return None
        token_data = schemas.TokenData(username=username, id=id, user_type=user_type)
    except JWTError:
        return None
    return token_data


def current_user_info(request: Request):
    token = request.cookies.get(constants.AUTH_TOKEN_COOKIE_NAME)
    if not token:
        return
    login = get_current_user_login(token)
    if not login:
        return
    if login.user_type == "admin":
        return crud.get_admin_by_id(login.id)
    if login.user_type == "technician":
        return crud.get_technician_by_id(login.id)
    raise NotImplementedError


def is_user_authenticated(request: Request,type: str='technician') -> bool:
    token = request.cookies.get(constants.AUTH_TOKEN_COOKIE_NAME)
    if not token:
        return False
    login = get_current_user_login(token)
    if login is None:
        return False
    if login.user_type != type:
            return False
    if login.user_type == "admin":
        if not crud.get_admin_by_id(login.id):
            return False
    if login.user_type == "technician":
        if not crud.get_technician_by_id(login.id):
            return False
    return True
