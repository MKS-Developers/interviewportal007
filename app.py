from flask import Flask, flash, render_template,jsonify,request,redirect,url_for
import firebase_admin
from firebase_admin import credentials, db, storage
import datetime
import os
import json


app = Flask(__name__)  # flask app object

cred = credentials.Certificate("key/interviewportal-007-firebase-adminsdk-myp3i-c8e47e4461.json")

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://interviewportal-007-default-rtdb.firebaseio.com",
    "storageBucket": "interviewportal-007.appspot.com",
})
app.secret_key = b'sriki007'  # for the flash messages we see for errors



#______Home______#
@app.route("/")
@app.route("/home")
def home():
	return render_template("views/home.html", title="Home")

#________Schedule________#

@app.route("/schedule")
def schedule():
	return render_template("views/schedule/schedule.html", title="Schedule")

@app.route("/viewSchedule", methods=['POST', 'GET'])
def viewSchedule():
  global viewScheduleData
  try:
    if request.method == 'POST':
      data = request.get_json()
      viewScheduleData = data['data']
      return jsonify(sucess=True)
    else:
      return render_template("views/schedule/viewSchedule.html", title="Edit Schedule", data=viewScheduleData)
  except Exception as e:
    flash('Oops..Invalid Route')
    return redirect(url_for('home'))

@app.route("/getScheduleData") # gives data to schedule route
def getScheduleData():
  try:
    temp = db.reference('students').get()
    print(temp)
    if type(temp) is dict:
      data = list(filter((None).__ne__, temp.values()))
    else:
      data = list(filter((None).__ne__, temp))
    # print(data)
    return jsonify(data)
  except Exception as error:
    print(error)
    flash(error)

@app.route("/database") # gives data to schedule route
def database():
  try:
    temp = open("key/database_model.json")
    data = json.load(temp)
    return jsonify(data)
  except Exception as error:
    print(error)
    flash(error)

@app.route("/resetDatabase") # gives data to schedule route
def resetDatabase():
  try:
    temp = open("key/database_model.json")
    data = json.load(temp)
    db.reference('/').set(data)
    flash('Database is now reset! Enjoy your testing')
    return redirect(url_for('home'))
  except Exception as error:
    print(error)
    flash(error)


@app.route("/bookInterview/<id>", methods=['GET', 'POST']) # gives data to schedule route
def bookInterview(id):
  try:
    if request.method == 'POST':
      file = request.files['resumePdf']
      candidateData = request.form.to_dict()
      temp = list(candidateData['availableon'].split('-'))
      temp2 = list(candidateData['availableFrom'].split(':'))
      temp3 = list(candidateData['scheduleTime'].split(':'))
      d = datetime.datetime(int(temp[0]),int(temp[1]),int(temp[2]),int(temp2[0]),int(temp[1]))

      v = datetime.datetime(int(temp[0]),int(temp[1]),int(temp[2]),int(temp3[0]),int(temp3[1]))
      if v>d:
          print('sdfghjkl;.')
          if file.filename != '':
            print(file.filename)
            filename = file.filename
            file.save(filename)
            print("@")
            temp, file_extension = os.path.splitext(filename)
            print("@")
            bucket = storage.bucket()
            blob = bucket.blob(f"Resumes/{id+file_extension}")
            print("@")
            blob.upload_from_filename(filename)
            print("@")
            blob.make_public()
            public_url = blob.public_url
            print(public_url)
            candidateData['resumeURL'] = public_url
            print("add to storage here")
            candidateData['id'] = id
            if os.path.isfile(filename):
                os.remove(filename)
            print('almost done')
            db.reference('upcoming').child(id).set(candidateData)
            db.reference('students').child(id).delete()
            flash('sucess')
            return redirect(url_for('schedule'))
      else:
        st = 'Timeslot ' +candidateData['scheduleTime'] +' is not avalable for ' + candidateData['name']
        flash(st)
        return redirect(url_for('schedule'))
        # return render_template("views/schedule/schedule.html", title="Schedule")

    else:
      flash('Oops.. invalid route')
      return redirect(url_for('home'))
  except Exception as error:
    flash(error)
    return redirect(url_for('home'))

#_________Upcoming_________#
@app.route("/upcoming")
def upcoming():
	return render_template("views/upcoming/upcoming.html", title="Upcoming")

@app.route("/viewUpcoming", methods=['POST', 'GET'])
def viewUpcoming():
  global viewUpcomingData
  try:
    if request.method == 'POST':
      data = request.get_json()
      viewUpcomingData = data['data']
      return jsonify(sucess=True)
    else:
      return render_template("views/upcoming/viewUpcoming.html", title="Edit Upcoming", data=viewUpcomingData)
  except Exception as e:
    print(e)
    flash('Oops..Invalid Route')
    return redirect(url_for('home'))



@app.route("/getUpcomingData") # gives data to schedule route
def getUpcomingData():
  try:
    temp = db.reference('upcoming').get()
    data = list(filter((None).__ne__, temp))

    return jsonify(data)
  except Exception as error:
    print(error)
    flash(error)

@app.route("/editInterview/<id>", methods=['GET', 'POST']) # gives data to upcoming route
def editInterview(id):
  try:
    print('inside edit')
    if request.method == 'POST':
      file = request.files['resumePdf']
      candidateData = request.form.to_dict()
      temp = list(candidateData['availableon'].split('-'))
      temp2 = list(candidateData['availableFrom'].split(':'))
      temp3 = list(candidateData['scheduleTime'].split(':'))
      d = datetime.datetime(int(temp[0]),int(temp[1]),int(temp[2]),int(temp2[0]),int(temp[1]))

      v = datetime.datetime(int(temp[0]),int(temp[1]),int(temp[2]),int(temp3[0]),int(temp3[1]))
      if v>d:
        print('sdfghjkl;.')
        if file.filename != '':
          print(file.filename)
          filename = file.filename
          file.save(filename)
          print("@")
          temp, file_extension = os.path.splitext(filename)
          print("@")
          bucket = storage.bucket()
          blob = bucket.blob(f"Resumes/{id+file_extension}")
          print("@")

          blob.upload_from_filename(filename)
          print("@")
          blob.make_public()
          public_url = blob.public_url
          print(public_url)
          candidateData['resumeURL'] = public_url
          print("add to storage here")
          if os.path.isfile(filename):
            os.remove(filename)
          print('almost done')
        candidateData['id'] = id
        db.reference('upcoming').child(id).update(candidateData)
        st = "Schedule of "+ candidateData['name']+" changed "+candidateData['scheduleTime']
        flash(st)
        print('success')
        return redirect(url_for('upcoming'))
      else:
        st = 'Timeslot ' +candidateData['scheduleTime'] +' is not avalable for ' + candidateData['name']
        flash(st)
        return redirect(url_for('upcoming'))
        # return render_template("views/upcoming/upcoming.html", title="Upcoming")

    else:
      flash('Oops.. invalid route')
      print('sdfghj')
      return redirect(url_for('home'))
  except Exception as error:
    print(error)
    flash(error)
    return redirect(url_for('home'))


if __name__ == '__main__':
	app.run(debug=True)



