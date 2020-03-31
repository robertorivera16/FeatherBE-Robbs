from flask import Flask, jsonify, request, make_response, send_from_directory, render_template, url_for
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message

from handlers.profile import ProfileHandler
from handlers.signup import SignUpHandler
from handlers.signin import SignInHandler
from handlers.dashboard import DashboardHandler
from handlers.explore import ExploreHandler
from handlers.professor import ProfessorHandler
from handlers.chart import ChartHandler
import jwt
import datetime
from functools import wraps
import random

# Import Cross-Origin Resource Sharing to enable
# services on other ports on this machine or on other
# machines to access this app

# Activate
app = Flask(__name__, template_folder='./templates')

app.config['SECRET_KEY'] = 'NbyaQXpd6gznqtQCu3tQqKTd'

# Apply CORS to this app
CORS(app)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'donotreply.feather.ilp@gmail.com',
    MAIL_PASSWORD = 'queue@#Bert',
))

mail = Mail(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        r = request
        token = request.headers.get('token')
        if token is None:
            return jsonify(Error="Token is missing"), 403
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify(Error="Token expired"), 403

        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
        if token is None:
            return jsonify(Error="Token is missing"), 403
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify(Error="Token is invalid"), 403

        if 'usertype' in payload:
            if int(payload['usertype']) != 1:
                return jsonify(Error="User is not admin"), 403
        else:
            return jsonify(Error="Token is invalid"), 403

        return f(*args, **kwargs)
    return decorated

@app.route('/')
@cross_origin()
def greeting():
    return 'Hello, this is the Feather App!'
#================================================Sign Up========================================#


@app.route('/Feather/signup/verification', methods=['POST'])
def getVerificationNum():
    if request.method == 'POST':
        print(request.json)
        randnum = random.randint(100000, 999999)
        subject = 'Verification Code DO NOT REPLY'
        sender = 'donotreply.feather.ilp@gmail.com'
        recipients=[request.json['email']]
        html_body=render_template('./verify_email.html',
                                             randnum=randnum,
                                             user=request.json['firstname'] + ' ' + request.json['lastname'])
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.html = html_body
        mail.send(msg)
        return jsonify(Code=randnum)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/Feather/professor/signup/init', methods=['GET'])
def getAllDepts():
    if request.method == 'GET':
        # print("REQUEST: ", request.json)
        return SignUpHandler().getAllDepts()
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/Feather/professor/signup', methods=['POST'])
def signUpProfessor():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return SignUpHandler().createNewProfessor(request.json)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/Feather/professor/signup/findemail/<string:email>', methods=['GET'])
def getProfPreData(email):
    if request.method == 'GET':
        if not email:
            return jsonify(Error="Missing parameter"), 400
        return SignUpHandler().getProfPreData(email)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/Feather/company/signup', methods=['POST'])
def signUpCompany():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return SignUpHandler().createNewEmployee(request.json)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/Feather/company/signup/init', methods=['GET'])
def getAllComps():
    if request.method == 'GET':
        # print("REQUEST: ", request.json)
        return SignUpHandler().getAllComps()
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/Feather/company/signup/<string:cname>', methods=['GET'])
def getCompPreData(cname):
    if request.method == 'GET':
        return SignUpHandler().getCompPreData(cname)
        print("REQUEST: ", cname)
    else:
        return jsonify(Error="Method not allowed."), 405

#=============================================Sign In=================================================
@app.route('/Feather/signin', methods=['POST'])
def signIn():
    if request.method == 'POST':
        email = request.json["email"]
        password = request.json["password"]

        if not email:
            return jsonify(Error="Missing username parameter"), 400
        if not password:
            return jsonify(Error="Missing password parameter"), 400

        result = SignInHandler().getUserData(email, password)

        if not result:
            return jsonify(Error='Invalid credentials'), 404

        payload = {
            'user': result[0],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=480),
            'usertype': result[1],
        }

        token = jwt.encode(payload, app.config['SECRET_KEY'])
        return jsonify(token=token.decode('UTF-8'), userid=result[0], usertype = result[1])

    else:
        return jsonify(Error="Method not allowed."), 405

#===================================Activities============================================
@app.route('/Feather/getactivitiesbydepartment', methods=['GET'])
def getActivitiesByDepartment():
    if request.method == 'GET':
        return DashboardHandler().getActivitiesByDepartment()
    else:
        return jsonify(Error="Method not allowed."), 405

#===========================Profile================================================
@app.route('/Feather/getprofilebyuserid/<userid>', methods=['GET'])
def getProfileByUserid(userid):
    if request.method == 'GET':
        return ProfileHandler().getProfileDataByUserId(userid)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/Feather/departments', methods=['GET'])
def getDepartments():
    r = request
    if request.method == 'GET':
        return ProfessorHandler().getDepartments()
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/Feather/editActsinProfile', methods=['POST'])
def editActsinProfile():
    if request.method == 'POST':
        return ProfileHandler().editActivitiesProfessorUserid(request.json)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/Feather/editProfile', methods=['POST'])
def editProfile():
    token = request.headers.get('token')
    if token is None:
        return jsonify(Error="Token is missing"), 403
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'])
    except:
        return jsonify(Error="Token is invalid"), 403

    if request.method == 'POST':
        return ProfileHandler().editProfileUserId(request.json, payload['user'])
    else:
        return jsonify(Error="Method not allowed."), 405
@app.route('/Feather/search', methods=['GET'])
def getBasicProfessorsProfile():
    if request.method == 'GET':
        q = request.args.get('q', type=str)
        profileType = request.args.get('profiletype', type=str)
        tag = request.args.get('tag', type=int)

        if profileType == 'professors':
             if q and tag:
                 return ExploreHandler().searchProfessorsProfileQT(q, tag)
             elif q:
                 return ExploreHandler().searchProfessorsProfileQ(q)
             elif tag:
                 return ExploreHandler().searchProfessorsProfileT(tag)
             else:
                 return ExploreHandler().getAllProfessorsProfiles()
        elif profileType == 'companies':
            if q and tag:
                return ExploreHandler().searchEmployeeProfileQT(q, tag)
            elif q:
                return ExploreHandler().searchEmployeeProfileQ(q)
            elif tag:
                return ExploreHandler().searchEmployeeProfileT(tag)
            else:
                return ExploreHandler().getAllEmployeeProfiles()
        else:
            return jsonify(Error="Missing arguments"), 405
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/Feather/tags', methods=['GET'])
def getAllTags():
    r = request
    print(request)
    if request.method == 'GET':
        return ExploreHandler().getAllTags()
    else:
        return jsonify(Error="Method not allowed"), 405

@app.route('/Feather/chart/<int:chartid>', methods=['GET'])
def getChartData(chartid):
    if request.method == 'GET':
        if chartid == 1:
            return ChartHandler().getCreatedUsersAccountsPerMonth()
        elif chartid == 2:
            return ChartHandler().getUpdatedUsersAccountsPerMonth()
        elif chartid == 3:
            return ChartHandler().getCreatedProfessorsProfilesPerMonth()
        elif chartid == 4:
            return ChartHandler().getUpdatedProfessorsProfilesPerMonth()
        elif chartid == 5:
            return ChartHandler().getUsersAccountsByDepartments()
        elif chartid == 6:
            return ChartHandler().getUsersAccountsByCompanies()
    else:
        return jsonify(Error="Method not allowed"), 405


#===============================================Run Main=======================================#
if __name__ == "__main__":
    # app.run(port=5000, host='0.0.0.0', debug=True)
    app.run()
