from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:dhirajMYSQL123@localhost/dbms_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define your Shelter model
class Shelter(db.Model):
    shelterID = db.Column(db.Integer, primary_key=True)
    shelterName = db.Column(db.String(50))
    location = db.Column(db.String(50))
    capacity = db.Column(db.Integer)
    contactInformation = db.Column(db.String(50))
    status = db.Column(Enum('Available', 'Nearing Capacity', 'At Capacity', name='shelter_status'))
    registrationDate = db.Column(db.Date)
    shelterType = db.Column(Enum('Emergency', 'Temporary', 'Long Term', name='shelter_type'))




@app.route('/')
def index():
    # Fetch data from the database
    AlappuzhaShelters = Shelter.query.filter_by(location='ALAPPUZHA').all()
    ErnakulamShelters = Shelter.query.filter_by(location='ERNAKULAM').all()
    ThrissurShelters = Shelter.query.filter_by(location='THRISSUR').all()
    shelters=[AlappuzhaShelters,ErnakulamShelters,ThrissurShelters]

    return render_template('index.html', shelters=shelters)


@app.route('/login')
def login():

    return render_template('login.html')

@app.route('/admin',methods=['POST','GET'])
def admin():
    # Retrieve username and password from the form
    username = request.form.get('username')
    password = request.form.get('password')

    #go to admin page if username and password is admin
    if(username=="admin" and password=="admin"):
        return render_template('admin.html')


if __name__ == '__main__':
    app.run(debug=True)
