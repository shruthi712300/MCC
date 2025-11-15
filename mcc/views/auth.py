from flask import (
    make_response,
    redirect,
    render_template,
    request,
    url_for,
    request,
)

from .. import app, crud, util, constants, schemas
from datetime import timedelta, datetime
import pytz


@app.get("/")
def login():
    # Check if it's already authenticate
    if util.is_user_authenticated(request) or util.is_user_authenticated(request, type="admin"):
        token = request.cookies.get(constants.AUTH_TOKEN_COOKIE_NAME)
        user = util.get_current_user_login(token)
        if user.user_type == "admin":
            return redirect(url_for("admin_dashboard"))
        elif user.user_type == "technician":
            return redirect(url_for("tech_dashboard"))
        else:
            return render_template("check.html", error_message="Invalid user type")
    return render_template("login.html")


@app.post("/")
def login_verify():
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role")
    if not util.is_valid_password(username, password, role):
        return render_template("check.html")
    access_token_expires = timedelta(days=constants.ACCESS_TOKEN_EXPIRE_DAYS)

    if role == "admin":
        admin_login = crud.get_admin(username=username)

        response = make_response(redirect(url_for("admin_dashboard")))

        jwt_token = util.create_access_token(
            schemas.TokenData(
                username=username,
                id=str(admin_login.admin_id),
                user_type="admin",
            ),
            access_token_expires,
        )

        response.set_cookie(
            constants.AUTH_TOKEN_COOKIE_NAME,
            jwt_token,
            expires=(datetime.now(pytz.timezone('Asia/Kolkata')) + access_token_expires),
        )
        return response

    elif role == "technician":
        technician_login = crud.get_technician(username=username)

        response = make_response(redirect(url_for("tech_dashboard")))

        jwt_token = util.create_access_token(
            schemas.TokenData(
                username=username,
                id=technician_login.technician_id,
                user_type="technician",
            ),
            access_token_expires,
        )

        response.set_cookie(
            constants.AUTH_TOKEN_COOKIE_NAME,
            jwt_token,
            expires=(datetime.now(pytz.timezone('Asia/Kolkata')) + access_token_expires),
        )
        return response
    else:
        return render_template("check.html", error_message="Invalid user type")


@app.get("/logout")
def logout():
    # remove the token from the cookie
    response = redirect(url_for("login"))
    response.set_cookie(constants.AUTH_TOKEN_COOKIE_NAME, "")
    return response
