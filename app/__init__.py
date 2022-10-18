from flask import Flask, redirect, url_for, request, render_template, flash, json, jsonify
import uuid
from flask_mongoengine import MongoEngine
from app.form_validator import validate_name, validate_street
import urllib 
import time
import os
app = Flask(__name__)

#DB_URI = "mongodb+srv://abhisec:"+urllib.parse.quote("Abhishek_!@#123")+"@vulnrpsys.cpamb0y.mongodb.net/vulnrpsys?retryWrites=true&w=majority"
app.config['SECRET_KEY'] = 'vulnrpsys'
#app.config["MONGODB_HOST"] = DB_URI
app.config['MONGODB_SETTINGS'] = {
    'db': 'vulnrpsys',
    'host': 'localhost',
    'port': 27017
}


#client = MongoClient('localhost', 27017)

#db = client.vulnrpsys
#researcher = db.researcher
db = MongoEngine()
db.init_app(app)

class Researcher(db.Document):
    r_id= db.StringField()
    firstname = db.StringField()
    lastname = db.StringField()
    dateofbirth = db.DateTimeField()
    street = db.StringField()
    city = db.StringField()
    state = db.StringField()
    zipcode = db.StringField()

class Organization(db.Document):
    org_id = db.StringField()
    org_name = db.StringField()
    org_domain = db.StringField()


'''@app.route('/temp')
def temp():
    researcher = Researcher.objects.all()
    return render_template('temp.html', researcher=researcher)'''

@app.route('/')
def query_records():
    researcher = Researcher.objects.all()
    return render_template('datatable.html', researcher=researcher)

@app.route('/organization')
def query_records_organization():
    organization = Organization.objects.all()
    return render_template('organization.html', organization=organization)


@app.route('/updateresearcher', methods=['POST','GET'])
def updateresearcher():
    if request.method == 'POST':
        r_id = request.form['txtr_id']  
        fname = request.form['txtfirstname']
        lname = request.form['txtlastname']
        dob = request.form['txtdateofbirth']
        street = request.form['txtstreet']
        city = request.form['txtcity']
        state = request.form['txtstate']
        zip = request.form['txtzipcode']
        researcher = Researcher.objects(r_id=r_id).first()
        if not researcher:
            return json.dumps({'error':'data not found'})
        else:
            researcher.update(firstname=fname, lastname=lname, dateofbirth=dob, street=street, city=city, state=state, zipcode=zip)
            flash(f'Updated Successfully:)', 'success')
            return redirect(url_for('query_records'))


@app.route('/updateorganization', methods=['POST','GET'])
def updateorganization():
    if request.method == 'POST':
        org_id = request.form['txtorg_id']  
        org_name = request.form['txtorg_name']
        org_domain = request.form['txtorg_domain']
        organization = Organization.objects(org_id=org_id).first()
        if not organization:
            return json.dumps({'error':'data not found'})
        else:
            organization.update(org_name=org_name, org_domain=org_domain)
            flash(f'Updated Successfully:)', 'success')
            return redirect(url_for('query_records_organization'))

@app.route('/delete/<string:getid>', methods = ['POST','GET'])
def delete_researcher(getid):
    print(getid)
    researchers = Researcher.objects(id=getid).first()
    if not researchers:
        return jsonify({'error': 'data not found'})
    else:
        researchers.delete() 
    return redirect('/')


@app.route('/delete/org/<string:getid>', methods = ['POST','GET'])
def delete_organization(getid):
    print(getid)
    organization = Organization.objects(id=getid).first()
    if not organization:
        return jsonify({'error': 'data not found'})
    else:
        organization.delete() 
    return redirect('/organization')




@app.route('/add', methods= ['POST'])
def index():
   #flash(f'You are already authenticated', 'danger')
   if request.method == 'POST':
      r_id = str(uuid.uuid4())
      r_id = r_id[0:8]
      fname = request.form['fname']
      lname = request.form['lname']
      dob = str(request.form['dob'])
      street = request.form['street']
      city = request.form['city']
      state = request.form['state']
      zip = request.form['zip']
      #researcher.insert_one({'r_id': r_id,'firstname': fname, 'lastname': lname, 'dateofbirth': dob, 'street': street, 'city': city, 'state': state, 'zipcode': zip})
      
      if validate_name(fname,3) is False:
        flash(f'Invalid Firstname', 'danger')
      elif validate_name(lname,3) is False:
        flash(f'Invalid Lastname', 'danger')
      elif validate_street(street) is False:
        flash(f'Invalid Street', 'danger')
      elif validate_name(city,3) is False:
        flash(f'Invalid City', 'danger')
      elif validate_name(state,3) is False:
        flash(f'Invalid State', 'danger')
      else:
        rssave = Researcher(r_id=r_id, firstname=fname, lastname=lname, dateofbirth=str(dob), street=street, city=city, state=state, zipcode=zip)
        rssave.save()
        flash(f'Data Inserted Successfully! ', 'success')
   return redirect(url_for('query_records')) 


@app.route('/addorg', methods= ['POST'])
def addorg():
   #flash(f'You are already authenticated', 'danger')
   if request.method == 'POST':
      org_id = str(uuid.uuid4())
      org_id = org_id[0:8]
      org_name = request.form['org_name']
      org_domain = request.form['org_domain']
      #researcher.insert_one({'r_id': r_id,'firstname': fname, 'lastname': lname, 'dateofbirth': dob, 'street': street, 'city': city, 'state': state, 'zipcode': zip})
      orgsave = Organization(org_id=org_id, org_name=org_name, org_domain=org_domain)
      orgsave.save()
      flash(f'Data Inserted Successfully! ', 'success')
   return redirect(url_for('query_records_organization')) 

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)