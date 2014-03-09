from flask import Flask, request, redirect, url_for, g, render_template, flash, session, abort,make_response
import sys,os
sys.path.append('sys/controller')
from authorhelper import *
from databasehelper import *
from circlehelper import *
DEBUG = True

dbhelper = Databasehelper()
ahelper = AuthorHelper()
chelper = CircleHelper()
dbhelper.connect()
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = os.urandom(24)
error = None
@app.route('/', methods=['GET', 'POST'])
def root():
	if 'logged_in' in session:
		return render_template('test1.html')
	else:
		return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username =request.form['username']
		password =request.form['password']
		if ahelper.authorauthenticate(dbhelper,username,password):
			session['logged_in'] = username
			error="login successful"
			re = make_response("True")
			re.headers['Content-Type']='text/plain'
			return re
		else:
			re = make_response("False")
			re.headers['Content-Type']='text/plain'
			return re
	return render_template('header.html')
@app.route('/register', methods=['PUT', 'POST'])
def register():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        nick_name=request.form['nick_name']
        if ahelper.addauthor(dbhelper,username,password,nick_name):
            re = make_response("True")
            session['logged_in'] = username
            re.headers['Content-Type']='text/plain'
            return re
        else:
            re = make_response("False")
            re.headers['Content-Type']='text/plain'
            return re
	return redirect(url_for('/'))

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	return redirect(url_for('login'))

# This is used to get friend list from database
@app.route('/post/getPermissionList',methods=['GET'])
def getPermissionList():
    	if request.method == 'GET':
		# Get the user ID from parameter
		userId = request.args.get('userid')
		# Use user ID to find user Name from database
		userName=ahelper.getnamebyid(dbhelper,userId)
		# Get the permission: friend or fof, from parameter 
		permission = request.args.get('option')
		if permission == "friend":
			friendlist=chelper.getfriendlist(dbhelper,userName)
			#return "friendlist: "+userId
			return friendlist
		elif permission == "fof":
			fof=chelper.getfriendoffriend(dbhelper,userName)
			#return "fof: " +userId
			return fof
		return "null"
	return "null"

# This is used to receive post target
@app.route('/post',methods=['PUT', 'POST'])
def post():
    	if request.method == 'POST':
		data = request.data
		return data
	return "null"

if __name__ == '__main__':
	app.debug = True
	app.run()
