# app routes

from flask import Flask,render_template,request,url_for,redirect
from flask import current_app as app
from backend.models import *
from datetime import datetime

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
            return redirect(url_for("admin_dashboard",name=uname))
        if usr and usr.role==1:
            return redirect(url_for("user_dashboard",name=uname))
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

    #many controllers/routers here

@app.route("/admin/<name>")
def admin_dashboard(name):
    theatres=get_theatres()
    return render_template("admin_dashboard.html",name=name,theatres=theatres)

@app.route("/user/<name>")
def user_dashboard(name):
    return render_template("user_dashboard.html",name=name)

#common route for admin dashboard
@app.route("/venue/<name>",methods=["POST","GET"])
def add_venue(name):
    if request.method=="POST":
        vname=request.form.get("name")
        location=request.form.get("location")
        pin_code=request.form.get("pin_code")
        capacity=request.form.get("capacity")
        new_theatre=Theatre(name=vname,location=location,pin_code=pin_code,capacity=capacity)
        db.session.add(new_theatre)
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))

    return render_template("add_venue.html",name=name)

@app.route("/show/<venu_id>/<name>",methods=["POST","GET"])
def add_show(venu_id,name):
    if request.method=="POST":
        sname=request.form.get("name")
        tags=request.form.get("tags")
        tkt_price=request.form.get("ticket_price")
        date_time=request.form.get("dt_time") #data is in string format
        #processing date time
        dt_time=datetime.strptime(date_time,"%Y-%m-%dT%H:%M")
        new_show=Show(name=sname,tags=tags,ticket_price=tkt_price,date_time=dt_time,theatre_id=venu_id)
        db.session.add(new_show)
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))
       
    return render_template("add_show.html",venu_id=venu_id,name=name)

@app.route("/search/<name>",methods=["GET","POST"])
def search(name):
    if request.method=="POST":
        search_txt=request.form.get("search_txt")
        by_venue=search_by_venue(search_txt)
        by_location=search_by_location(search_txt)
        if by_venue:
            return render_template("admin_dashboard.html",name=name,theatres=by_venue)
        elif by_location:
            return render_template("admin_dashboard.html",name=name,theatres=by_location)

    return redirect(url_for("admin_dashboard",name=name))








#other supported fuction
def get_theatres():
    theatres=Theatre.query.all()
    return theatres

def search_by_venue(search_txt):
    theatres=Theatre.query.filter(Theatre.name.ilike(f"%{search_txt}%")).all()
    return theatres

def search_by_location(search_txt):
    theatres=Theatre.query.filter(Theatre.location.ilike(f"%{search_txt}%")).all()
    return theatres
