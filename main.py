from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, ForeignKey

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:dhirajMYSQL123@localhost/dbms_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Badass Kalidas'
AdminUsername="Admin"
AdminPassword="Admin"
AdminLoggedin=False

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


class Person(db.Model):
    PersonID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(25))
    LastName = db.Column(db.String(25))
    DOB = db.Column(db.Date)
    Age = db.Column(db.Integer)
    Gender = db.Column(Enum('Male', 'Female', name='gender_enum'))
    ContactInformation = db.Column(db.String(50))
    EmergencyContact = db.Column(db.String(25))
    Address = db.Column(db.String(50))
    EntryDate = db.Column(db.Date)
    ExitDate = db.Column(db.Date)
    Status = db.Column(Enum('Active', 'Inactive', name='status_enum'))
    ShelterID = db.Column(db.Integer)
    

class Staff(db.Model):
    StaffID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(25))
    LastName = db.Column(db.String(25))
    DOB = db.Column(db.Date)
    Gender = db.Column(Enum('Male', 'Female', name='gender_enum'))
    ContactInformation = db.Column(db.String(50))
    Address = db.Column(db.String(50))
    Salary = db.Column(db.DECIMAL(10,2), default=None)
    Position = db.Column(db.String(25))
    EmploymentStatus = db.Column(Enum('Part Time', 'Full Time', name='employment_status_enum'))
    DateOfHire = db.Column(db.Date)
    Shift = db.Column(Enum('Day', 'Night', name='shift_enum'))
    ShelterID = db.Column(db.Integer)

class Inventory(db.Model):
    ItemID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ItemName = db.Column(db.String(25))
    Category = db.Column(Enum('Food', 'Clothing', 'Medical', 'Other', name='category_enum'))
    Quantity = db.Column(db.Integer)
    UnitOfMeasure = db.Column(db.String(25))
    ExpirationDate = db.Column(db.Date)
    DateReceived = db.Column(db.Date)
    Conditions = db.Column(Enum('New', 'Used', 'Expired', name='conditions_enum'))
    CostPerUnit = db.Column(db.DECIMAL(10,2))
    AvailabilityStatus = db.Column(Enum('1', '2', '3', '4', '5', name='availability_status_enum'))
    ShelterID = db.Column(db.Integer)



@app.route('/')
def index():
    global AdminLoggedin
    AdminLoggedin=False
    # Fetch data from the database
    AlappuzhaShelters = Shelter.query.filter_by(location='ALAPPUZHA').all()
    ErnakulamShelters = Shelter.query.filter_by(location='ERNAKULAM').all()
    ThrissurShelters = Shelter.query.filter_by(location='THRISSUR').all()
    shelters=[AlappuzhaShelters,ErnakulamShelters,ThrissurShelters]

    return render_template('index.html', shelters=shelters)


@app.route('/login')
def login():
    global AdminLoggedin
    AdminLoggedin=False
    return render_template('login.html')

@app.route('/admin',methods=['POST','GET'])
def admin():
    global AdminLoggedin
    # Fetch data from the Shelter table
    alpy = Shelter.query.filter_by(location='ALAPPUZHA').all()
    ekm = Shelter.query.filter_by(location='ERNAKULAM').all()
    tsr = Shelter.query.filter_by(location='THRISSUR').all()
    print("ALAPPUZHA Shelters:", alpy)
    print("ERNAKULAM Shelters:", ekm)
    print("THRISSUR Shelters:", tsr)
    if AdminLoggedin:
        return render_template('admin.html', alpy=alpy, ekm=ekm, tsr=tsr)
    elif request.method == 'POST':
        # Retrieve username and password from the form
        username = request.form.get('username')
        password = request.form.get('password')

        #go to admin page if username and password is admin
        if(username=="admin" and password=="admin"):
            AdminLoggedin=True
            return render_template('admin.html', alpy=alpy, ekm=ekm, tsr=tsr)
        
        else:
            flash('Invalid Credentials! Login Failed!', 'error')
    return redirect(url_for('login'))


@app.route('/insert', methods=['POST','GET'])
def insert():
    return render_template('insert.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST' and 'shelter_register_button' in request.form:
        shelter_name = request.form['ShelterName']
        location = request.form['Location']
        capacity = request.form['Capacity']
        contact_information = request.form['ContactInformation']
        registration_date = request.form['RegistrationDate']
        status = request.form['Status']
        shelter_type = request.form['ShelterType']

        new_shelter = Shelter(shelterID=404,shelterName=shelter_name, location=location, capacity=capacity,
                              contactInformation=contact_information, registrationDate=registration_date,
                              status=status, shelterType=shelter_type)

        db.session.add(new_shelter)
        db.session.commit()

    if request.method == 'POST' and 'person_register_button' in request.form:
        first_name = request.form['FirstName']
        last_name = request.form['LastName']
        dob = request.form['DOB']
        gender = request.form['Gender']
        contact_information = request.form['ContactInformation']
        emergency_contact = request.form['EmergencyContact']
        address = request.form['Address']
        entry_date = request.form['EntryDate']
        exit_date = request.form['ExitDate']
        status = request.form['Status']
        shelter_id = request.form['ShelterID']

        new_person = Person(
            FirstName=first_name,
            LastName=last_name,
            DOB=dob,
            Gender=gender,
            ContactInformation=contact_information,
            EmergencyContact=emergency_contact,
            Address=address,
            EntryDate=entry_date,
            ExitDate=exit_date,
            Status=status,
            ShelterID=shelter_id
        )

        db.session.add(new_person)
        db.session.commit()
        
    if request.method == 'POST' and 'staff_register_button' in request.form:
        first_name = request.form['FirstName']
        last_name = request.form['LastName']
        dob = request.form['DOB']
        gender = request.form['Gender']
        contact_information = request.form['ContactInformation']
        address = request.form['Address']
        position = request.form['Position']
        employment_status = request.form['EmploymentStatus']
        date_of_hire = request.form['DateOfHire']
        shift = request.form['Shift']
        shelter_id = request.form['ShelterID']

        new_staff = Staff(
            FirstName=first_name,
            LastName=last_name,
            DOB=dob,
            Gender=gender,
            ContactInformation=contact_information,
            Address=address,
            Position=position,
            EmploymentStatus=employment_status,
            DateOfHire=date_of_hire,
            Shift=shift,
            ShelterID=shelter_id
        )

        db.session.add(new_staff)
        db.session.commit()
        
    if request.method == 'POST' and 'inventory_register_button' in request.form:
        item_name = request.form['ItemName']
        category = request.form['Category']
        quantity = request.form['Quantity']
        unit_of_measure = request.form['UnitOfMeasure']
        expiration_date = request.form['ExpirationDate']
        date_received = request.form['DateReceived']
        cost_per_unit = request.form['CostPerUnit']
        availability_status = request.form['AvailabilityStatus']
        shelter_id = request.form['ShelterID']

        new_inventory = Inventory(
            ItemName=item_name,
            Category=category,
            Quantity=quantity,
            UnitOfMeasure=unit_of_measure,
            ExpirationDate=expiration_date,
            DateReceived=date_received,
            CostPerUnit=cost_per_unit,
            AvailabilityStatus=availability_status,
            ShelterID=shelter_id
        )

        db.session.add(new_inventory)
        db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
