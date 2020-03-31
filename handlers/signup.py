"""
This is the handler that connects the http request inputs to the DAOs
in an organized format for better implementation
@Author: Angel G. Carrillo Laguna
@git: AngelGCL
@date_of_creation: October 1st, 2019
"""
from flask import jsonify
from daos.signup import signupDAO

class SignUpHandler:

    #===============================================Professors=============================================#
    #This will create a data structure that helps organize the information returned from the DAO
    def buildProfessorAttributes(self, row):
        dao = signupDAO()
        result = {}
        result['profid'] = row[0]
        result['firstname'] = row[1]
        result['lastname'] = row[2]
        result['acadpos'] = row[3]
        result['depid'] = dao.getDepartmentbyId(row[4])
        return result

    def buildProfessorAttributes2(self):
        dao = signupDAO()
        result = {}
        result['profid'] = '1'
        result['firstname'] = 'Angel'
        result['lastname'] = 'Carrillo'
        result['acadpos'] = 'Professor'
        result['depid'] = dao.getDepartmentbyId('1')
        return result

    def buildActivityAttributes(self, row):
        result = {}
        result['actid'] = row[0]
        result['actname'] = row[1]
        result['ongoing'] = row[2]
        result['fundrange'] = row[3]
        result['actdate'] = row[4]
        result['description'] = row[5]
        return result

#TO-DO: Add the newActivity functions

    def getAllDepts(self):
        dao = signupDAO()
        result = dao.getAllDepts()
        if not result:
            # Val is a variable to determine wether the profile exists or not
            return jsonify(Error='Departments not found.'), 404
        else:
            return jsonify(Departments=result), 200

    def getAllComps(self):
        dao = signupDAO()
        result = dao.getAllComps()
        if not result:
            # Val is a variable to determine wether the profile exists or not
            return jsonify(Error='Companies not found.'), 404
        else:
            return jsonify(Companies=result), 200

    def getProfPreData(self, email):
        dao = signupDAO()
        result = dao.getProfessorPreData(email)
        if not result:
            # Val is a variable to determine wether the profile exists or not
            return jsonify(Error='Professor not found.', Val='0'), 404
        else:
            prof = self.buildProfessorAttributes(result)
            return jsonify(Professor=prof, Val='1'), 200

    def createNewProfessor(self, json):
        dao = signupDAO()
        val = json['Val']
        if val == 0:
            new_profile = dao.insertProfessor(json)
            return jsonify(new_profile), 200
        else:
            new_user = dao.updateProfessor(json)
            return jsonify(Success='Account created'), 200

    #===========================================Companies=========================================#

    #Will create a dictionary for the front end to read the information of the PRE-DATA
    def buildCompanyAttributes(self, row):
        result = {}
        result['cid'] = row[0]
        result['cname'] = row[1]
        return result

    def getCompPreData(self, cname):
        dao = signupDAO()
        result = dao.companyPreData(cname)
        if not result:
            return jsonify(Error='Company not found.'), 404
        else:
            comp = self.buildCompanyAttributes(result)
            return jsonify(Company = comp), 200

    def createNewEmployee(self, json):
        dao = signupDAO()
        new_profile = dao.insertEmployee(json)
        return jsonify(new_profile), 200