"""
This is the handler that connects the http request inputs to the DAOs
in an organized format for better implementation
@Author: Angel G. Carrillo Laguna
@git: AngelGCL
@date_of_creation: October 1st, 2019
"""
from flask import jsonify
from daos.dashboard import DashboardDAO

class DashboardHandler:

    # Helper method to build dictionary 
    def buildActivitiesByDepartment(self,rows):
        result = {}
        result['actid'] = rows[0]
        result['actname'] = rows[1]
        result['dname'] = rows[2]
        return result

    def getActivitiesByDepartment(self):
        dao = DashboardDAO()
        result = dao.getActivitiesByDepartment()
        if not result:
            return jsonify(Error='Activities not found'), 404
        mapped_result = []
        for r in result:
            mapped_result.append(self.buildActivitiesByDepartment(r))
        return jsonify(mapped_result)
