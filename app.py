# starting of app
from flask import Flask 
from backend.models import db

app=None

def setup_app():
    app=Flask(__name__)
   
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///ticket_show.sqlite3" #having db file

    # pending here is sqlite connection
    db.init_app(app) #flask app connected to db(sql alchemy)
    app.app_context().push()  #direct access to other module
    app.debug=True
    print("ticket show app started")

#call set_up
setup_app()




from backend.controllers import *

if __name__=="__main__":
    app.run()