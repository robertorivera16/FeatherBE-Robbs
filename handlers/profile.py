from flask import jsonify
from daos.signin import signinDAO
from handlers.employee import EmployeeHandler
from handlers.professor import ProfessorHandler


# Wrapper class to return either Employee Profile information or Professor Information to fill out profile
class ProfileHandler:

    def getProfileDataByUserId(self, userid):
        handler = EmployeeHandler()
        data = handler.getEmployeeDataByUserid(userid)
        if not data:
            #Try searching in Professors Table
            handler = ProfessorHandler()
            data = handler.getProfessorDataByUserid(userid)
            if not data:
                return jsonify(Error='Profile not found')
        return data

    def editActivitiesProfessorUserid(self, json):
        userid = json['userid']
        handler = ProfessorHandler()
        handler.editActivity(json)
        data = handler.getProfessorDataByUserid(userid)
        if not data:
            return jsonify(Error='Profile not found')
        return data

    def editProfileUserId(self, json, userid):

        handler = EmployeeHandler()
        data = handler.setEmployeeDataByUserid(userid, json)
        if not data:
            # Try searching in Professors Table
            handler = ProfessorHandler()
            data = handler.setProfessorDataByUserid(userid, json)
            if not data:
                return jsonify(Error='Profile not found')
        return data

