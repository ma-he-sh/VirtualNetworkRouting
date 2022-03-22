
from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.dialects.sqlite

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fit.sqlite'
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False

db = SQLAlchemy(app)

class fit(db.Model):
    _id = db.Column("id" , db.Integer, primary_key=True)
    source_no = db.Column(db.Integer)
    destination_no = db.Column(db.Integer)
    cost = db.Column(db.Integer)

    def __init__(self,source_no,destination_no,cost):
            self.source_no = source_no
            self.destination_no = destination_no
            self.cost = cost

@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/", methods= ["POST", "GET"])
def login():
        return render_template("index.html")

@app.route("/total", methods=["POST", "GET"])
def total():
    if request.method == "POST":
        total= request.form["Node"]
        return render_template("cost.html", total= total)
    else:
        return 404


@app.route("/grab", methods=["POST", "GET"])
def grab():
    if request.method == "POST":
        source = request.form.getlist("source[]")
        destination = request.form.getlist("destination[]")
        distt = request.form.getlist("dist[]")
        for i in range(0,10):
            for y in source:
                for z in destination:
                    for x in distt:
                        if (source.index(y)==i and destination.index(z)==i and distt.index(x)==i):
                            add = fit(y,z,x)
                            db.session.add(add)
                            db.session.commit()
        return render_template("dist.html", values = fit.query.all())    
                
    else:
        return "Invalid"

if __name__ == "__main__":
    db.create_all()
    app.run()
    


"""0: {node1: 'A', node2: 'B', cost: 12}

    1: {node1: 'A', node2: 'C', cost: NaN}
    2: {node1: 'A', node2: 'D', cost: 123}
    3: {node1: 'A', node2: 'E', cost: 123}
    4: {node1: 'B', node2: 'C', cost: NaN}
    5: {node1: 'B', node2: 'D', cost: 123}
    6: {node1: 'B', node2: 'E', cost: 123}
    7: {node1: 'C', node2: 'D', cost: 123}
    8: {node1: 'C', node2: 'E', cost: 123}
    9: {node1: 'D', node2: 'E', cost: 1231}"""