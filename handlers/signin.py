from flask import jsonify
from daos.signin import signinDAO

class SignInHandler:

    #===============================================Professors=============================================#
    #This will create a data structure that helps organize the information returned from the DAO
    def buildUser(self, row):
        result = {}
        result['userid'] = row[0]
        result['usertype'] = row[1]
        return result

#TO-DO: Add the newActivity functions

    def getUserData(self, email, password):
        dao = signinDAO()
        result = dao.getUserData(email, password)
        return result
        """
        if not result:
            return jsonify(Error='User not found.'), 404
        else:
            prof = self.buildUser(result)
            return jsonify(User=prof), 200
        """

    def getUserType(self, userid):
        dao = signinDAO()
        result = dao.getUserType(userid)
        return result
