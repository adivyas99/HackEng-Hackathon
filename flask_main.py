import os
from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from models import *


@app.route("/")
def ping():
	return "ping resp"
#register and login
@app.route("/register",methods=['POST'])
def register():
	email_ = request.form['email']
	password_ = request.form['password']
	name_ = request.form['name']
	location_ = request.form['location']
	gender_ = request.form['gender']
	interest_ = request.form['interest']
	college_ = request.form['college']
	number = request.form['number']
	print(email_)
	print(password_)
	try:
		credentials = Credentials(email = email_, password = password_)
		db.session.add(credentials)
		db.session.commit()
		profile = User_Profile(email = email_,name = name_,location = location_,gender = gender_,interest = interest_,college = college_,mentor = False, number = number)
		db.session.add(profile)
		db.session.commit()
		return"ok"
		
	except Exception as e:
		return str(e)
'''
@app.route("/login",methods=['POST'])
def login():
	email = request.form['email']
	password = request.form['password']
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			return "True"
		else:
			return "False"
	except Exception as e:
		print(str(e))
		return ste(e)
#setter functions

@app.route("/enroll", methods=['POST'])
def enroll():
	email = request.form['email']
	password = request.form['password']
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			enrollment = Enrollment(
					mentee = email,
					mentor = None,
					status = 1,
					topic_name = request.form['topic_name']
				)
			mList= Mentor_list.query.filter_by(topic_name=request.form['topic_name']).all()
			for name in mList:
				notif = Notification(
						sender = email,
						recipient = name.email,
						request = False,
						topic_name = request.form['topic_name']
					)
				db.session.add(notif)
			db.session.add(enrollment)
			db.session.commit()
			return "True"
		else:
			print("no exception fail")
			return "False"
	except Exception as e:
		print(str(e))
		return "False"
@app.route("/add_timeline", methods=['POST'])
def add_timeline():
	email = request.form['email']
	password = request.form['password']
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			timeline = Timeline(
					topic_name = request.form['topic_name'],
					day = request.form['day'],
					goal = request.form['goal'],
					mentor = request.form['email'],
					link = request.form['link']
				)
			db.session.add(timeline)
			db.session.commit()
			return 'True'
		else:
			return 'False'
	except Exception as e:
		print(str(e))
		return 'False'
@app.route("/add_mentor", methods=['POST'])
def add_mentor():
	email = request.form['email']
	password = request.form['password']
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			if Topics.query.filter_by(topic_name=request.form['topic_name']).first() is None:
				topic = Topics(topic_name = request.form['topic_name'])
				db.session.add(topic)
				db.session.commit()
			mentor = Mentor_list(
					topic_name = request.form['topic_name'],
					email = request.form['email']
				)
			user = User_Profile.query.filter_by(email = email).first()
			user.mentor=True
			db.session.add(mentor)
			db.session.commit()
			return 'True'
		else:
			return 'False'
	except Exception as e:
		print(str(e))
		return 'False'
@app.route("/add_topics", methods=['POST'])
def new_topic():
	email = request.form['email']
	password = request.form['password']
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			user = User_Profile.query.filter_by(email = email).first()
			if user.mentor:
				topic = Topics(
					topic_name = request.form['topic_name']
				)
				db.session.add(topic)
				db.session.commit()
				return "True"
			else :
				return "you are not a mentor"
		else:
			return "False"
	except Exception as e:
		print(str(e))
		return "False"
@app.route("/add_request", methods=['POST'])
def new_request():
	email = request.form['email']
	password = request.form['password']
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			req = New_requests(
					topic_name = request.form['topic_name'],
					requester =  email
				)
			db.session.add(req)
			db.session.commit()
			return "True"
		else:
			return "False"
	except Exception as e:
		return(str(e))
@app.route("/pick_request", methods=['POST'])
def pick_request():
	email = request.form['email']
	password = request.form['password']
	print(email, password)
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			mentor = Mentor_list(
					topic_name = request.form['topic_name'],
					email = request.form['email']
				)
			db.session.add(mentor)
			topic = Topics(
					topic_name = request.form['topic_name']
				)
			db.session.add(topic)
			New_requests.query.filter_by(topic_name=request.form['topic_name']).delete()
			db.session.commit()
			return "added"
		else:
			return "failed"
	except Exception as e:
		print(str(e))
		return str(e)
@app.route("/change_status", methods=['POST'])
def change_status():
	email = request.form['email']
	password = request.form['password']
	print(email, password)
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			data = Enrollment.query.filter_by(mentee =request.form['mentee'] ).filter_by(topic_name=request.form['topic_name']).first()
			print(str(data.status))
			data.status+=1
			data.mentor=email
			db.session.commit()
			return "added"
		else:
			return "failed"
	except Exception as e:
		print(str(e))
		return str(e)
@app.route("/notification_status", methods=['POST'])
def notification_status():
	email = request.form['email']
	password = request.form['password']
	print(email, password)
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			data = Notification.query.filter_by(sender =request.form['sender'] ).filter_by(recipient = email).filter_by(topic_name=request.form['topic_name']).first()
			print(str(data.request))
			data.request=True
			db.session.commit()
			notif = Notification(
					sender = email,
					recipient = request.form['sender'],
					request = True,
					topic_name = request.form['topic_name']
				)
			return "added"
		else:
			return "failed"
	except Exception as e:
		print(str(e))
		return str(e)

#getter functions____________________________________________________________________________________________________________________
@app.route("/enrollment_status", methods=['POST'])
def enrollment_status():
	email = request.form['email']
	password = request.form['password']
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			detail = Enrollment.query.filter_by(mentee = email).filter_by(topic_name = request.form['topic_name']).first();
			print(detail)
			if(detail.mentor == None):
				return "False"
			else :
				return str(detail.mentor)
	except Exception as e:
		print(str(e))
		return str(e)
@app.route("/profile",methods=['POST'])
def profile():
	email = request.form['email']
	password = request.form['password']
	print(email, password)
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			profile = User_Profile.query.filter_by(email = email).first()
			print(str(profile))
			dict={
					"email": str(profile.email),
					"name": str(profile.name),
					"interest": str(profile.interest),
					"location": str(profile.location),
					"gender" :str(profile.gender),
					"college": str(profile.college),
					"number": str(profile.number),
					"mentor":str(profile.mentor)
				}
			return jsonify(dict)
		else:
			return "failed"
	except Exception as e:
		print(str(e))
		return str(e)
@app.route("/diffprofile",methods=['POST'])
def diffprofile():
	email = request.form['email']
	password = request.form['password']
	print(email, password)
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			profile = User_Profile.query.filter_by(email = request.form['new_email']).first()
			print(str(profile))
			dict={
					"email": str(profile.email),
					"name": str(profile.name),
					"interest": str(profile.interest),
					"location": str(profile.location),
					"gender" :str(profile.gender),
					"college": str(profile.college),
					"number": str(profile.number),
					"mentor":str(profile.mentor)
				}
			return jsonify(dict)
		else:
			return "failed"
	except Exception as e:
		print(str(e))
		return str(e)
@app.route("/get_topics",methods=['POST'])
def topic_list():
	email = request.form['email']
	password = request.form['password']
	print(email, password)
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			topics = Topics.query.all()
			topic_list={}
			i=0
			for topic in topics:
				print(str(topic.topic_name))
				topic_list.update({str(i):str(topic.topic_name)})
				i+=1
			return jsonify(topic_list)
		else:
			return "failed"
	except Exception as e:
		print(str(e))
		return str(e)
@app.route("/get_mentor_details",methods=['POST'])
def mentor_details():
	email = request.form['email']
	password = request.form['password']
	print(email, password)
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			details = Enrollment.query.filter_by(mentor= email).all()
			print(str(details))
			detail_list={}
			i=0
			for detail in details:
				print(str(detail))
				detail_list.update({str(i):{"mentee":str(detail.mentee),"topic":str(detail.topic_name),"status":str(detail.status)}})
				i+=1
			return jsonify(detail_list)
		else:
			return "failed"
	except Exception as e:
		print(str(e))
		return str(e)
@app.route("/get_mentee_details",methods=['POST'])
def mentee_details():
	email = request.form['email']
	password = request.form['password']
	print(email, password)
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			details = Enrollment.query.filter_by(mentee= email).all()
			print(str(details))
			detail_list={}
			i=0
			for detail in details:
				print(str(detail))
				detail_list.update({str(i):{"mentee":str(detail.mentor),"topic":str(detail.topic_name),"status":str(detail.status)}})
				i+=1
			return jsonify(detail_list)
		else:
			return "failed"
	except Exception as e:
		print(str(e))
		return str(e)

@app.route("/get_timeline",methods=['POST'])
def get_timeline():
	email = request.form['email']
	password = request.form['password']
	print(email, password)
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			details = Timeline.query.filter_by(topic_name =request.form['topic_name'] ).all()
			print(str(details))
			detail_list={}
			i=0
			for detail in details:
				print(str(detail))
				detail_list.update({str(i):{"mentor":str(detail.mentor),"day":str(detail.day),"goal":str(detail.goal),"topic":str(detail.topic_name),"link":str(detail.link)}})
				i+=1
			return jsonify(detail_list)
		else:
			return "failed"
	except Exception as e:
		print(str(e))
		return str(e)
@app.route("/get_timeline_sp",methods=['POST'])
def get_timeline_sp():
	email = request.form['email']
	password = request.form['password']
	print(email, password)
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			details = Timeline.query.filter_by(topic_name =request.form['topic_name'] ).filter_by(mentor= request.form['mentor']).all()
			print(str(details))
			detail_list={}
			i=0
			for detail in details:
				print(str(detail))
				detail_list.update({str(i):{"mentor":str(detail.mentor),"day":str(detail.day),"goal":str(detail.goal),"topic":str(detail.topic_name),"link":str(detail.link)}})
				i+=1
			return jsonify(detail_list)
		else:
			return "failed"
	except Exception as e:
		print(str(e))
		return str(e)
@app.route("/get_notifications",methods=['POST'])
def get_notifications():
	email = request.form['email']
	password = request.form['password']
	print(email, password)
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			details = Notification.query.filter_by(recipient= request.form['email']).all()
			print(str(details))
			detail_list={}
			i=0
			for detail in details:
				print(str(detail))
				detail_list.update({str(i):{"sender":str(detail.sender),"details":str(detail.topic_name)}})
				i+=1
			return jsonify(detail_list)
		else:
			return "failed"
	except Exception as e:
		print(str(e))
		return str(e)
@app.route("/get_applied",methods=['POST'])
def get_applied():
	email = request.form['email']
	password = request.form['password']
	print(email, password)
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			details = Enrollment.query.filter_by(mentee = email).all()
			print(str(details))
			detail_list={}
			i=0
			for detail in details:
				print(str(detail))
				detail_list.update({str(i):{"topic_name":str(detail.topic_name)}})
				i+=1
			return jsonify(detail_list)
		else:
			return "failed"
	except Exception as e:
		print(str(e))
		return str(e)
@app.route("/get_mentors",methods=['POST'])
def get_mentors():
	email = request.form['email']
	password = request.form['password']
	print(email, password)
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			details = Mentor_list.query.all()
			print(str(details))
			detail_list={}
			i=0
			for detail in details:
				print(str(detail))
				detail_list.update({str(i):{"mentor":str(detail.email),"topic_name":str(detail.topic_name)}})
				i+=1
			return jsonify(detail_list)
		else:
			return "failed"
	except Exception as e:
		print(str(e))
		return str(e)
@app.route("/get_requests",methods=['POST'])
def get_request_list():
	email = request.form['email']
	password = request.form['password']
	print(email, password)
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			reqs = New_requests.query.all()
			topic_list={}
			i=0
			for topic in reqs:
				print(str(topic.topic_name))
				topic_list.update({str(i):{"topic":str(topic.topic_name),"requester":str(topic.requester)}})
				i+=1
			return jsonify(topic_list)
		else:
			return "failed"
	except Exception as e:
		print(str(e))
		return str(e)
@app.route("/getspMentor",methods=['POST'])
def spMentor():
	email = request.form['email']
	password = request.form['password']
	print(email, password)
	try:
		credentials=Credentials.query.filter_by(email = email).first()
		if password == str(credentials.password):
			mentors = Enrollment.query.filter_by(mentee = email).filter(Enrollment.mentor != None).all()
			mentor_list={}
			i=0
			for mentor in mentors:
				print(str(mentor.mentor))
				mentor_list.update({str(i):{"mentor":str(mentor.mentor),"topic":str(mentor.topic_name)}})
				i+=1
			return jsonify(mentor_list)
		else:
			return "failed"
	except Exception as e:
		print(str(e))
		return str(e)

# change status 
migrate = Migrate(app, db)
if __name__ == '__main__':
	app.run()
#localhost:5000/register?email="root"&password="root"&name="qwerty"&location="qwerty"&gender="male"&interest="qwerty"&college="qwerty"
#curl -v -H "Content-Type: application/json" -X POST \ -d '{"email":"root","password":"root","name":"qwerty","location":"qwerty","gender":"male","interest":"qwerty","college":"qwerty"}' http://127.0.0.1:5000/register
    
'''