# app routes

from flask import Flask,render_template,request
from flask import current_app as app
from backend.models import *

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method=="POST":
        uname=request.form.get("user_name")
        pwd=request.form.get("password")
        usr=User_info.query.filter_by(email=uname,password=pwd).first()
        if usr and usr.role==0:
            return render_template("admin_dashboard.html")
        if usr and usr.role==1:
            return render_template("user_dashboard.html")
        else:
            return render_template("login.html",msg="invalid user")

    return render_template("login.html",msg="")

@app.route("/register",methods=["POST","GET"])
def signup():
    if request.method=="POST":
        uname=request.form.get("user_name")
        pwd=request.form.get("password")
        full_name=request.form.get("full_name")
        address=request.form.get("location")
        pin_code=request.form.get("pin_code")
        usr=User_info.query.filter_by(email=uname,password=pwd).first()
        if usr:
            return render_template("signup.html",msg="sorry,user already exist")
        new_usr=User_info(email=uname,password=pwd,full_name=full_name,address=address,pin_code=pin_code)
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html",msg="Thank You,Try Login")

    return render_template("signup.html",msg="")